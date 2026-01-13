import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="LLM Document Q&A",
    page_icon="📄",
    layout="centered"
)

# -------------------------
# Initialize Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #DCF8C6;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 8px;
    width: fit-content;
    max-width: 80%;
}
.chat-bubble-ai {
    background-color: #F1F0F0;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    width: fit-content;
    max-width: 80%;
}
.source-box {
    font-size: 0.85em;
    color: #555;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("⚙️ Session & Upload")

    session_id = st.text_input(
        "Session ID",
        value="demo1",
        help="Same session ID maintains conversation memory"
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "📤 Upload PDF Document",
        type=["pdf"]
    )

    if uploaded_file and st.button("Ingest Document"):
        with st.spinner("Ingesting document..."):
            files = {"file": uploaded_file}
            response = requests.post(
                f"{BACKEND_URL}/documents/ingest",
                files=files
            )

        data = response.json()

        if "error" in data:
            st.error(data["error"])
            st.session_state.messages = []
            st.session_state.document_ready = False
        else:
            st.success("Document ingested successfully!")
            st.session_state.messages = []
            st.session_state.document_ready = True

    st.divider()

    if st.button("🔄 Reset Conversation"):
        response = requests.post(
            f"{BACKEND_URL}/session/reset",
            json={"session_id": session_id}
        )
        if response.status_code == 200:
            st.success("Session reset.")
            st.session_state.messages = []
        else:
            st.error(response.text)

# -------------------------
# Main Header
# -------------------------
st.title("📄 LLM-Based Document Q&A")
st.caption("Retrieval-Augmented Generation with Conversation Memory")

# -------------------------
# Display Chat History
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'><b>You:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble-ai'><b>AI:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )
        if msg.get("sources"):
            st.markdown(
                f"<div class='source-box'>📌 Sources: {', '.join(msg['sources'])}</div>",
                unsafe_allow_html=True
            )

# -------------------------
# Chat Input
# -------------------------
st.divider()

if not st.session_state.document_ready:
    st.warning("Please upload a valid text-based PDF document before asking questions.")
else:
    query = st.text_input("💬 Ask a question about the document")

    if st.button("Ask"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": query
            })

            with st.spinner("Thinking..."):
                payload = {
                    "session_id": session_id,
                    "query": query
                }
                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json=payload
                )

            if response.status_code == 200:
                data = response.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", [])
                })
                st.rerun()
            else:
                st.error(response.text)
