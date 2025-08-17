from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import src.backend.config as config

#1. Load the documents
loader = TextLoader("data/docs.txt")
docs = loader.load()

#2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

#3. Embeddings
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

#4. Connect to Qdrant Client
client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)

QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name=config.COLLECTION_NAME,
    client=client
)

print("✅ Documents ingested into Qdrant!")