import streamlit as st
import ollama
import chromadb
from chromadb.utils import embedding_functions

# --- Setup ---
st.set_page_config(page_title="Crohn Helper AI Agent", layout="wide")

# Initialize Chroma (local, persistent)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Use Ollama embeddings (make sure you have an embedding model, e.g. `nomic-embed-text`)
ollama_embeddings = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text"
)

# Create / get collection
collection = chroma_client.get_or_create_collection(
    name="docs",
    embedding_function=ollama_embeddings
)

# --- Simple example: insert docs (only once) ---
if "initialized" not in st.session_state:
    documents = [
        "Crohn's disease is a type of inflammatory bowel disease (IBD) "
        "that causes chronic inflammation of the digestive tract. "
        "It can affect any part of the GI tract, from the mouth to the anus, "
        "but most commonly affects the small intestine and the beginning of "
        "the large intestine.",
        "Symptoms vary, but often include abdominal pain, diarrhea, fatigue,"
        "and weight loss. There's currently no cure, but treatments can help"
        "manage symptoms and prevent complications according to the NHS.",
        "Risk Factors:Family history, smoking, and certain medications can increase "
        "the risk of developing Crohn's disease. "
    ]
    for i, doc in enumerate(documents):
        collection.add(documents=[doc], ids=[str(i)])
    st.session_state.initialized = True

# --- Streamlit UI ---
st.title("💬 Crohn Helper AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Step 1: embed query & retrieve docs
    results = collection.query(query_texts=[prompt], n_results=3)
    context = "\n".join(results["documents"][0])

    # Step 2: send to Ollama
    full_prompt = f"Use the following context to answer:\n\n{context}\n\nQuestion: {prompt}"
    stream = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": full_prompt}],
        stream=True
    )

    # Step 3: stream response to UI
    response_container = st.chat_message("assistant")
    placeholder = response_container.empty()

    response_text = ""
    with st.spinner("Assistant is typing..."):  # show spinner while generating
        for chunk in stream:
            token = chunk["message"]["content"]
            response_text += token
            placeholder.markdown(response_text)

    # Save final message
    st.session_state.messages.append({"role": "assistant", "content": response_text})