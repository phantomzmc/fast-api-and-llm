# FastAPI and LLM Integration Project

This project demonstrates how to build a powerful API using FastAPI and integrate it with Ollama for locally hosted Large Language Models (LLMs). It provides a foundation for creating intelligent, AI-powered services that can leverage the capabilities of modern language models without relying on external cloud services.

## Project Overview

This project explores the synergy between FastAPI, a modern, high-performance web framework for building APIs with Python, and locally hosted LLMs through Ollama. By combining these technologies, we can create APIs that:

* **Process Natural Language:** Understand and respond to user queries in natural language
* **Generate Text:** Create various forms of text content, such as summaries, articles, code, and more
* **Perform Complex Tasks:** Handle tasks like sentiment analysis, text classification, question answering, and more
* **Support Multilingual Applications:** Process and generate text in multiple languages, including Thai

## Architecture

The project uses a Docker Compose setup with three main services:

1. **FastAPI Application (`app`)**: The core API service built with FastAPI that handles requests and communicates with the LLM service
2. **Ollama Service (`ollama`)**: A locally hosted LLM server running Ollama that processes language tasks
3. **Nginx Reverse Proxy (`nginx`)**: Routes traffic to the appropriate services

All services communicate over a shared Docker network (`network_poc_llm`).

## Features

* **FastAPI-Powered API:** Leverages FastAPI's speed, efficiency, and ease of use for building robust APIs
* **Local LLM Integration:** Seamlessly integrates with Ollama for hosting LLMs locally, providing privacy and cost advantages
* **Multi-container Architecture:** Uses Docker Compose to manage multiple interconnected services
* **Clear API Endpoints:** Defines well-structured API endpoints for interacting with the LLM
* **Persistent Model Storage:** Uses Docker volumes to maintain model data between restarts
* **Input Validation:** Uses FastAPI's built-in validation with Pydantic to ensure data integrity
* **Chat Interface:** Supports both one-shot completions and chat-based interactions with the LLM
* **Multilingual Support:** Works with multiple languages, including Thai

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic health check endpoint |
| `/items/{item_id}` | GET | Example endpoint with path and query parameters |
| `/health-check-llm` | GET | Check connection to LLM and list available models |
| `/ask` | GET | Simple completion endpoint for one-shot questions |
| `/ask/chat` | GET | Demonstrates chat-based interaction with examples |
| `/chat` | POST | Main chat endpoint that accepts user messages |

## Getting Started

### Prerequisites

* **Docker and Docker Compose:** For containerized deployment
* **Git:** For cloning the repository

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Create the external Docker network:**
   ```bash
   docker network create network_poc_llm
   ```

3. **Build and start the services:**
   ```bash
   docker-compose up -d
   ```

4. **Access the API:**
   The API will be available at `http://localhost:80` or directly at `http://localhost:8000`

### Installing Ollama Locally (Alternative to Docker)

If you prefer to run Ollama directly on your host machine instead of using Docker:

1. **Install Ollama:**
   
   **For Linux:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   
   **For macOS:**
   - Download from https://ollama.com/download/mac
   - Open the downloaded file and follow installation instructions
   
   **For Windows:**
   - Download from https://ollama.com/download/windows
   - Run the installer and follow the instructions

2. **Start the Ollama service:**
   ```bash
   ollama serve
   ```
   This starts the Ollama server on port 11434

3. **Update the FastAPI configuration:**
   If running Ollama locally, change the `LLM_BASE_URL` in `main.py`:
   ```python
   LLM_BASE_URL = "http://127.0.0.1:11434"  # Local Ollama server
   # LLM_BASE_URL = "http://ollama_server:11434"  # Comment out or remove this line
   ```

### Loading Models

Ollama supports various LLM models. To load and use a specific model:

1. **Load a model using Docker:**
   ```bash
   # If using Docker setup
   docker exec -it ollama_server ollama pull llama3.2:1b
   ```

2. **Load a model on local Ollama installation:**
   ```bash
   # If using local Ollama installation
   ollama pull llama3.2:1b
   ```

3. **Available models:**
   You can use various models depending on your needs:
   - `llama3.2:1b` - Small 1B parameter model (fastest)
   - `llama3.2:8b` - Medium 8B parameter model (balanced)
   - `llama3.2:70b` - Large 70B parameter model (most capable)
   - `gemma:2b` - Google's 2B parameter model
   - `phi3:3.8b` - Microsoft's Phi-3 model
   
   For a complete list of available models:
   ```bash
   # In Docker
   docker exec -it ollama_server ollama list
   
   # Or locally
   ollama list
   ```

4. **Update the model in configuration:**
   To use a different model, update the `MODEL_NAME` variable in `main.py`:
   ```python
   MODEL_NAME = "llama3.2:8b"  # Change to your desired model
   ```

## Usage Examples

### Basic Health Check
```bash
curl http://localhost/health-check-llm
```

### Ask a Question
```bash
curl http://localhost/ask
```

### Chat with the LLM
```bash
curl -X POST http://localhost/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the advantages of using local LLM models?"}'
```

## Development

To develop and extend this project:

1. **Local Development Setup:**
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate     # On Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run the FastAPI application locally:**
   ```bash
   uvicorn main:app --reload
   ```

Note: When running locally, you may need to adjust the `LLM_BASE_URL` in `main.py` to point to your local Ollama instance.

## Docker Details

### Volumes
* `ollama_data`: Persists LLM models between container restarts

### Networks
* `network_poc_llm`: External network for communication between containers

## License

[Your license information here]

## Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Ollama](https://ollama.ai/) - For providing the local LLM server
* [Llama](https://ai.meta.com/llama/) - For the open-source LLM model