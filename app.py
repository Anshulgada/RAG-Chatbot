from fastapi import FastAPI, UploadFile
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
import os
import tempfile


class ChatRequest(BaseModel):
    message: str


rag_pipeline = None

llm = None
embed_model = None
device = "cpu"


@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm, embed_model, device
    # Load the RAG pipeline
    device = (
        f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu"
    )
    print(f"Using device: {device}")

    # Create embeddings
    model_name = "sentence-transformers/all-mpnet-base-v2"
    embed_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={"device": device, "batch_size": 32},
    )

    # Load the language model
    llm = LlamaCpp(
        model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
        n_gpu_layers=-1,
        n_batch=512,
        n_ctx=2048,
        f16_kv=True,
        verbose=False,
    )
    print("LLM and embedding model loaded.")
    yield
    # Clean up resources if needed
    llm = None
    embed_model = None
    print("LLM and embedding model unloaded.")


app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins (for development purposes only)
    allow_origins=["http://localhost:3000"],  # Allows the React frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: UploadFile = None):
    global rag_pipeline
    try:
        if file is None:
            # Use the default Harry Potter PDF
            file_path = "Harry Potter and the Sorcerers Stone.pdf"
            print(
                "No file uploaded. Using default file: Harry Potter and the Sorcerers Stone.pdf"
            )
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                file_path = tmp.name

        loader = PyPDFLoader(file_path)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_documents(data)
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=embed_model)

        rag_pipeline = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )
        print(f"RAG pipeline created for {file.filename if file else 'default file'}")
        return {"message": "File uploaded and processed successfully."}
    except Exception as e:
        return {"error": f"Failed to process file: {e}"}
    finally:
        if file and "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)


@app.post("/chat")
async def chat(chat_request: ChatRequest):
    if rag_pipeline is None:
        return {"error": "Please upload a PDF first."}

    response = rag_pipeline(chat_request.message)
    return {"reply": response["result"]}


@app.get("/")
async def root():
    return {"message": "Backend is running."}
