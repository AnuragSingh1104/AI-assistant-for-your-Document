# src/summary.py

from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

persist_dir = r"C:\Users\Anurag\Desktop\AI assistant-EZ LABS\data\chroma_db"

@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model="BAAI/bge-large-en-v1.5",
        encode_kwargs={"normalize_embeddings": True}
    )

@st.cache_resource
def get_vectorstore():
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    return vectorstore

@st.cache_resource
def get_llm():
    llm = ChatOllama(
        model="mistral",
        temperature=0.2,   # concise summary
        top_p=0.95
    )
    return llm

def summary_pdf():
    llm = get_llm()
    vectorstore = get_vectorstore()

    # Retrieve top docs for "summary"
    query = "summary"
    retrieved_docs = vectorstore.similarity_search(query, k=3)

    # Build context
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # System prompt
    system_prompt = f"""
    You are an expert summarizer bot.

    Your task is to write a clear and concise summary of the following content, using no more than 150 words.

    Context:
    {context}

    Instructions:
    - Keep the summary under 150 words.
    - Focus on the key points only.
    - Write in clear and simple language.
    """

    # Messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Generate the summary.")
    ]

    # Invoke LLM
    response = llm(messages)

    return response.content
