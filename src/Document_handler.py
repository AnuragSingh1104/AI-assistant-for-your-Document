
import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st

persist_dir = r"C:\Users\Anurag\Desktop\AI assistant-EZ LABS\data\chroma_db"

# Cache the embedding model
@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(
        model="BAAI/bge-large-en-v1.5",
        encode_kwargs={"normalize_embeddings": True}
    )

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Extract text from TXT
def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()

# Load all text files in uploads folder
def load_all_texts(folder_path):
    text = ""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.lower().endswith(".pdf"):
            text += extract_text_from_pdf(file_path)
        elif file_name.lower().endswith(".txt"):
            text += extract_text_from_txt(file_path)
        else:
            print(f"Unsupported file format: {file_name}")
    return text

# Split text into chunks
def split_text(raw_text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    return text_splitter.split_text(raw_text)

# Main doc_handler
def doc_handler():
    embedding_model = load_embedding_model()

    # If vectorstore already exists → load it
    if os.path.exists(os.path.join(persist_dir, "index")):
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_model
        )
    else:
        raw_text = load_all_texts(r"uploads")
        split_doc = split_text(raw_text)

        vectorstore = Chroma.from_texts(
            texts=split_doc,
            embedding=embedding_model,
            persist_directory=persist_dir
        )
        vectorstore.persist()
        print("Vectorstore created and persisted successfully.")
    return vectorstore
