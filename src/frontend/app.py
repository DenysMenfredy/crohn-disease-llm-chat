import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from src.backend.rag_pipeline import build_rag_pipeline
from src.backend.streaming_callback import StreamHandler

# --- Setup ---
st.set_page_config(page_title="💬 Crohn Helper AI Agent", layout="wide")
st.title("💬 Crohn Helper AI Agent")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Chat input ---
if prompt := st.chat_input("Ask me anything about Crohn's disease..."):
    # User message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Assistant streaming response (simulate chunking)
    response_container = st.chat_message("assistant")
    placeholder = response_container.empty()

    #Spinner while LLM is thinking
    with st.spinner("Assistant is typing..."):
        # Attach streaming handler
        handler = StreamHandler(placeholder)
        qa = build_rag_pipeline(callbacks=[handler])
        result = qa.invoke(prompt)
    
    # Finalize assistant message
    final_text = handler.text.strip()
    st.session_state.messages.append({"role": "assistant", "content": final_text})
