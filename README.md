# RAG PDF Chatbot

## Overview

RAG PDF Chatbot is a Retrieval-Augmented Generation (RAG) chatbot built using FastAPI and Llama-2. It processes PDF documents and allows users to interact with the content through a conversational interface. The project leverages advanced language models and embeddings to provide accurate and context-aware responses.

## Features

- Load and process PDF documents.
- Generate embeddings using `sentence-transformers`.
- Use `Chroma` as a vector store for efficient retrieval.
- Integrate with Llama-2 for natural language understanding and generation. (Can use any other open source model in gguf format or even replace with LMStudio)
- FastAPI backend with endpoints for chat and health checks.
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
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

5. Navigate to the frontend directory and start the React app:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Usage

- Access the backend at `http://0.0.0.0:8000`.
- Use the `/chat` endpoint to send chat messages and receive responses.
- Open the frontend at `http://localhost:3000` for a user-friendly interface.

## Project Structure

- `app.py`: FastAPI backend implementation.
- `frontend/`: React-based frontend.
- `models/`: Directory for storing the Llama-2 model.
- `Harry Potter and the Sorcerers Stone.pdf`: Sample PDF for testing.
- `pyproject.toml`: Project dependencies and configuration.

## Author

Anshul Gada
