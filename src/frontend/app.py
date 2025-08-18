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

# Function to display a message card (ChatGPT-style)
def display_message(role, content):
    if role == "user":
        bg_color = "#DCF8C6"
        icon = "🧑"
    else:
        bg_color = "#F1F0F0"
        icon = "🤖"

    html = f"""
    <div style="
        background-color:{bg_color};
        color:#000000;
        padding:12px 16px;
        border-radius:12px;
        margin:6px 0px;
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size:15px;
        line-height:1.4;
        box-shadow:0px 1px 3px rgba(0,0,0,0.1);
        max-width:80%;
        white-space:pre-wrap;
    ">
        <span style="margin-right:6px; font-size:18px;">{icon}</span>{content}
    </div>
    """
    container = st.empty()
    container.markdown(html, unsafe_allow_html=True)
    return container

# --- Render existing messages only once ---
for i, msg in enumerate(st.session_state.messages):
    if "container" not in msg:
        container = display_message(msg["role"], msg["content"])
        st.session_state.messages[i]["container"] = container

# --- Chat input ---
if prompt := st.chat_input("Ask me anything about Crohn's disease..."):
    # Display user message immediately
    user_container = display_message("user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "container": user_container})

    # Prepare assistant placeholder
    assistant_placeholder = st.empty()
    st.session_state.messages.append({"role": "assistant", "content": "", "container": assistant_placeholder})

    # Stream assistant response
    with st.spinner("Assistant is typing..."):
        handler = StreamHandler(
            messages_list=[st.session_state.messages[-1]],
            placeholder=assistant_placeholder
        )
        qa = build_rag_pipeline(callbacks=[handler])
        qa.invoke(prompt)
