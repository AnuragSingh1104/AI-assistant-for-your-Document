# 🤖 AI Assistant for Your Document

A **private, local AI assistant** that helps you **search**, **summarize**, and **interact with your documents** (PDF or TXT) using **Large Language Models (LLMs)** — completely offline on your machine.

Built with **LangChain**, **ChromaDB**, **Hugging Face embeddings**, and **Ollama**, this project enables:

✅ Automatic **document processing**  
✅ Accurate **semantic search**  
✅ Natural language **Q&A**  
✅ **Summary generation**  
✅ **Quiz creation**  

And — your documents **never leave your machine** 🚀.

---

## 🧐 What This Project Does

Many AI apps send your documents to a cloud server (ChatGPT, Gemini, etc.). This project lets you:

1. Upload a PDF/TXT to a local app
2. Process & embed the document into a vector store (ChromaDB)
3. Use a local LLM (Ollama + Mistral) to:
    - Generate summaries
    - Answer any questions about the document
    - Generate quiz questions
4. All of this works **offline**, on your machine — so your data stays private.

---

## ✨ Features

✅ **Document Processing:** PDF + TXT → Cleaned text → Split into semantic chunks  
✅ **Vector Storage:** ChromaDB — Fast local vector database  
✅ **Embeddings:** Uses **Hugging Face BAAI/bge-large-en-v1.5** embeddings  
✅ **Retrieval-Augmented Generation (RAG):** Combines retrieval with local LLM for better answers  
✅ **Local LLMs:** Mistral or other Ollama models — no internet required  
✅ **Streamlit UI:** Simple interface for upload, processing, interaction  
✅ **Private:** No data leaves your laptop  
✅ **Extensible:** Modular code — easy to customize

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai) installed and running locally  
  _(You can pull a model with: `ollama pull mistral`)_

---

### 2️⃣ Installation

```bash
# Clone the repo
git clone https://github.com/AnuragSingh1104/AI-assistant-for-your-Document.git

# Change into project directory
cd AI-assistant-for-your-Document

# Install required Python packages
pip install -r requirements.txt
