# Crohn Disease LLM Chat

This project provides a chat interface powered by a Large Language Model (LLM) to assist with information and support related to Crohn's Disease.

## Features

- Interactive chat for Crohn's Disease queries
- Powered by state-of-the-art LLM
- User-friendly interface using Streamlit

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/denys7/crohn-disease-llm-chat.git
    cd crohn-disease-llm-chat
    ```

2. **Install dependencies and activate a virtual environment (recommended):**
    ```bash
    uv sync
    source .venv/bin/activate
    ```

3. **Set up a docker container running [Qdrant](https://qdrant.tech/documentation/quickstart/) Vector DB:**
    ```bash
    docker pull qdrant/qdrant
    docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
    ```
4. **Set up Ollama for local LLM access:**
    - Install [Ollama](https://ollama.com/download)
    ```bash
        ollama pull mistral #choose the model you want
    ```
## Usage

1. **Ingest the data in the vector DB for RAG:**
    ```bash
    python src/backend/ingest.py
    ```

2. **Run the chat application using Streamlit:**
    ```bash
    streamlit run src/frontend/app.py
    ```

3. **Access the chat interface:**
    - Open your browser and go to the URL provided by Streamlit (e.g., `http://localhost:8501`).

## Configuration

- Edit `src/backend/config.py` to adjust the environment variables.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, open an issue or contact the maintainer at [GitHub Issues](https://github.com/denys7/crohn-disease-llm-chat/issues).