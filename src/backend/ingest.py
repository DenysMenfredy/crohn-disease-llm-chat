import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
import src.backend.config as config

def ingest_data(data_folder="data"):
    """
    Reads all .txt files from `data_folder`, splits them into chunks,
    embeds them, and stores them in Qdrant.
    """
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(model=config.EMBEDDING_MODEL)
    sample_vector = embeddings.embed_query("test")
    vector_size = len(sample_vector)

    # Connect to Qdrant
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)

    # Create/recreate collection
    if not client.collection_exists(config.COLLECTION_NAME):
        client.create_collection(
            config.COLLECTION_NAME,
            vectors_config={ "size": vector_size, "distance": "Cosine" }
        )

    # Initialize vector store
    db = QdrantVectorStore(
        client=client,
        collection_name=config.COLLECTION_NAME,
        embedding=embeddings
    )

    # Iterate through all text files
    total_docs = 0
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()

            if not text:
                continue

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            chunks = text_splitter.split_text(text)

            # Add chunks to Qdrant
            ids = list(range(len(chunks)))
            db.add_texts(texts=chunks, ids=ids)
            total_docs += len(chunks)

    print(f"Ingested {total_docs} document chunks into collection '{config.COLLECTION_NAME}'.")


ingest_data("data")