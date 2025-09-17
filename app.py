from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from contextlib import asynccontextmanager

class ChatRequest(BaseModel):
    message: str

rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline
    # Load the RAG pipeline
    device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load and process the PDF
    loader = PyPDFLoader("Harry Potter and the Sorcerers Stone.pdf")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    # Create embeddings and vector store
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={'device': device, 'batch_size': 32}
    )
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=embed_model)

    # Load the language model
    llm = LlamaCpp(
        model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
        n_gpu_layers=-1,
        n_batch=512,
        n_ctx=2048,
        f16_kv=True,
        verbose=False,
    )

    # Create the RAG pipeline
    rag_pipeline = RetrievalQA.from_chain_type(
        llm=llm, chain_type='stuff',
        retriever=vectorstore.as_retriever()
    )
    print("RAG pipeline loaded.")
    yield
    # Clean up resources if needed
    rag_pipeline = None
    print("RAG pipeline unloaded.")

app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allows the React frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    if rag_pipeline is None:
        return {"error": "RAG pipeline is not loaded."}
    
    response = rag_pipeline(chat_request.message)
    return {"reply": response['result']}

@app.get("/")
async def root():
    return {"message": "Backend is running."}
