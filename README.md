# RAG PDF Chatbot

## Overview

RAG PDF Chatbot is a Retrieval-Augmented Generation (RAG) chatbot built using FastAPI and Llama-2. It processes PDF documents and allows users to interact with the content through a conversational interface. The project leverages advanced language models and embeddings to provide accurate and context-aware responses.

## Features

- Load and process PDF documents.
- Upload PDF files dynamically via the frontend.
- Generate embeddings using `sentence-transformers`.
- Use `Chroma` as a vector store for efficient retrieval.
- Integrate with Llama-2 for natural language understanding and generation. (Can use any other open source model in gguf format or even replace with LMStudio)
- FastAPI backend with endpoints for chat, file upload, and health checks.
- Next.js-based frontend for user interaction.

## Prerequisites

- Python 3.10 or higher
- CUDA-enabled GPU (optional, for faster processing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Anshulgada/RAG-Chatbot.git
   cd RAG-Chatbot
   ```

2. Install dependencies (recommend using uv package manager):

   ```bash
   uv venv
   uv sync
   ```

3. Ensure the Llama-2 model file is placed in the `models/` directory:

   - File: `llama-2-7b-chat.Q4_K_M.gguf`

4. Start the FastAPI server:

   ```bash
   uvicorn app:app --reload
   ```

5. Navigate to the frontend directory and start the React app:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Usage

- Access the backend at `http://0.0.0.0:8000`.
- Use the `/upload` endpoint to upload a PDF file for processing.
- Use the `/chat` endpoint to send chat messages and receive responses.
- Open the frontend at `http://localhost:3000` for a user-friendly interface.

### Frontend Features

- **File Upload**: Upload a PDF file directly from the interface.
- **Chat Interface**: Type messages and receive responses in real-time.
- **Responsive Design**: Optimized for both light and dark modes.

### Backend Endpoints

- `POST /upload`: Upload a PDF file for processing.
- `POST /chat`: Send a chat message and receive a response.
- `GET /`: Health check endpoint.

## Project Structure

- `app.py`: FastAPI backend implementation.
- `frontend/`: React-based frontend.
- `models/`: Directory for storing the Llama-2 model.
- `Harry Potter and the Sorcerers Stone.pdf`: Sample PDF for testing.
- `pyproject.toml`: Project dependencies and configuration.

## Additional Notes

### Llama-CPP-Python

For further details and updates on `llama-cpp-python`, refer to the following resources:

- [PyPI: llama-cpp-python](https://pypi.org/project/llama-cpp-python/)
- [LangChain Documentation: LlamaCPP](https://python.langchain.com/docs/integrations/llms/llamacpp/)

### CUDA Toolkit

Before installing PyTorch, ensure that the CUDA Toolkit is downloaded and installed. The version of the CUDA Toolkit must match the version of PyTorch you are installing. For example, if PyTorch is version `12.8`, the CUDA Toolkit should also be version `12.8`.

- For the latest CUDA Toolkit, visit: [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
- If you need an older version of the CUDA Toolkit, visit: [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)

At the time of writing, the latest CUDA Toolkit version is `13`, while the latest PyTorch version is `12.9`. Ensure compatibility by downloading the appropriate versions.

### Torch Installation

Torch should be installed based on your system configuration. For Windows machines using CUDA and Python, visit the [PyTorch Get Started](https://pytorch.org/get-started/locally/) page to find the appropriate installation command.

For example, if you are using CUDA version `cu128`, the installation command would be:

```bash
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

Replace `cu128` with the current CUDA version available at the time. Always refer to the PyTorch website for the latest instructions.

## Author

Anshul Gada
