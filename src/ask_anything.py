# src/ask_anything.py

from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st

persist_dir = r"C:\Users\Anurag\Desktop\AI assistant-EZ LABS\data\chroma_db"

# 1. Cache embedding model
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model="BAAI/bge-large-en-v1.5",
        encode_kwargs={"normalize_embeddings": True}
    )

# 2. Cache vectorstore
@st.cache_resource
def get_vectorstore():
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    return vectorstore

# 3. Cache Ollama LLM
@st.cache_resource
def get_llm():
    llm = ChatOllama(
        model="mistral",
        temperature=0.1,
        top_p=0.95,
    )
    return llm

# 4. Setup Conversation Chain (cached)
@st.cache_resource
def get_conversation_chain():
    llm = get_llm()
    vectorstore = get_vectorstore()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

    return conversation_chain

# Main ask_anything
def ask_anything(question):
    conversation_chain = get_conversation_chain()

    response = conversation_chain.invoke({
        "question": question,
        "chat_history": conversation_chain.memory.chat_memory.messages
    })

    return response["answer"]
