import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from modules.text_processing import extract_text
from modules.vector_store import build_vectorstore
from modules.qa_chain import create_qa_chain

# ---------------------
# Gen Z Branding
# ---------------------
APP_NAME = "✨ Askify AI ✨"
TAGLINE = "Your docs, your convo 🗂️💬"

st.set_page_config(page_title=APP_NAME, page_icon="🤖", layout="wide")

# ---------------------
# Sidebar
# ---------------------
with st.sidebar:
    st.title("⚡ Quick Settings")
    st.markdown("Welcome to **DocTalks AI** 👋")
    st.markdown("Upload your files & chat like never before!")
    st.markdown("---")
    st.subheader("🌐 Connect with Me")
    st.markdown("[GitHub](https://github.com/hamzasheraz) | [LinkedIn](https://www.linkedin.com/in/hamza-sheraz-/)")

# ---------------------
# Header / Landing
# ---------------------
st.markdown(
    f"""
    <div style="text-align: center; padding: 40px 10px;">
        <h1 style="font-size: 3em; margin-bottom: 0;">{APP_NAME}</h1>
        <p style="font-size: 1.2em; color: gray;">{TAGLINE}</p>
        <p style="font-size: 1em; color: #9b59b6;">🚀 Built with LangChain, FAISS & OpenAI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------
# File Upload
# ---------------------
uploaded_files = st.file_uploader(
    "📂 Upload your files (PDF, TXT, DOCX)", 
    type=["pdf", "txt", "docx"], 
    accept_multiple_files=True
)

# ---------------------
# CSS Styling
# ---------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f9f9ff 0%, #e6f7ff 100%);
    }
    .user-bubble {
        background: rgba(0, 200, 150, 0.15);
        padding: 12px 18px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-align: right;
        font-family: 'Segoe UI';
        font-size: 15px;
    }
    .assistant-bubble {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        padding: 12px 18px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-align: left;
        font-family: 'Trebuchet MS';
        font-size: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------
# Main Logic
# ---------------------
if uploaded_files:
    all_text = ""
    for uploaded_file in uploaded_files:
        all_text += extract_text(uploaded_file)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(all_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    vectorstore = build_vectorstore(docs)
    qa_chain = create_qa_chain(vectorstore)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

    # Input
    if user_input := st.chat_input("💬 Ask DocTalks AI anything..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

        result = qa_chain.invoke({"question": user_input})
        answer = result["answer"]

        st.markdown(f"<div class='assistant-bubble'>🤖 {answer}</div>", unsafe_allow_html=True)

        if result.get("source_documents"):
            st.markdown("### 📌 Sources")
            for i, source_doc in enumerate(result["source_documents"], 1):
                st.markdown(f"**{i}.** {source_doc.page_content[:200]}...")

        st.session_state.messages.append({"role": "assistant", "content": answer})
