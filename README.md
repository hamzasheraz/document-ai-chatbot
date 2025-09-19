# 📚 Document AI Assistant

An AI-powered chatbot that lets you upload your documents (PDF, TXT, DOCX) and ask questions in natural language.  
Built with **LangChain, FAISS, OpenAI API, and Streamlit**.

## 🚀 Features
- 📂 Upload multiple documents
- 💬 Multi-turn chat (memory enabled)
- 📌 Source citations for transparency
- 🎨 Streamlit chat UI
- ☁️ Easy deployment (Streamlit Cloud)

## 🛠️ Tech Stack
- Python, Streamlit
- LangChain + FAISS
- OpenAI API
- PyPDF2, python-docx

## ⚡ Setup
```bash
git clone <your-repo>
cd rag-chatbot
pip install -r requirements.txt
streamlit run app.py
set OPENAI_KEY variable in .env
