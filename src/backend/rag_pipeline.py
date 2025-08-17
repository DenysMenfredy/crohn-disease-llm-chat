from langchain import hub
from langchain_ollama import OllamaLLM
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import src.backend.config as config
from qdrant_client import QdrantClient

def build_rag_pipeline(callbacks=None):
    embeddings = HuggingFaceEmbeddings(model=config.EMBEDDING_MODEL)

    client = QdrantClient(
        host=config.QDRANT_HOST,
        port=config.QDRANT_PORT,
    )


    db = QdrantVectorStore(
        client=client,
        collection_name=config.COLLECTION_NAME,
        embedding=embeddings,
    )

    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = OllamaLLM(model="mistral", callbacks=callbacks or [])

    prompt = hub.pull("rlm/rag-prompt")

    qa = (
        {
            "context": retriever,
            "question":RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa