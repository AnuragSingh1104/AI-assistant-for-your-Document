# src/challenge_me.py

from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st

persist_dir = r"C:\Users\Anurag\Desktop\AI assistant-EZ LABS\data\chroma_db"

# Cache LLM
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="mistral",
        temperature=0.1,
        top_p=0.95,
    )

# Cache embedding model + vectorstore
@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(
        model="BAAI/bge-large-en-v1.5",
        encode_kwargs={"normalize_embeddings": True}
    )

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )
    return vectorstore

def generate_quiz():
    llm = get_llm()
    vectorstore = get_vectorstore()

    # Retrieve context docs
    query = "important concepts"
    retrieved_docs = vectorstore.similarity_search(query, k=5)

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    # System prompt
    system_prompt = f"""
    You are a quiz master bot.

    Your job is to read the context below (from a PDF), and generate 3 different quiz questions that test understanding of the material.

    Context:
    {context}

    Instructions:
    - Generate exactly 3 quiz questions.
    - Make the questions varied and thoughtful.
    - Do not give answers or explanations, only the questions.
    - Format:
      1. Question 1
      2. Question 2
      3. Question 3
    """

    # Ollama expects a string prompt:
    final_prompt = f"""
    {system_prompt}

    Generate the quiz questions.
    """

    response = llm.invoke(final_prompt)

    return response.content, context  # return context for later checking

def evaluate_answer(user_answer, correct_context):
    llm = get_llm()

    system_prompt = f"""
    You are an expert evaluator bot.

    Here is the correct context from the document:
    {correct_context}

    The user gave this answer:
    {user_answer}

    Your job is:
    - Evaluate if the answer is correct.
    - If correct, say "✅ Correct!" and give short praise.
    - If incorrect, say "❌ Incorrect." and briefly explain what is missing.
    - Be short and clear.
    """

    final_prompt = f"""
    {system_prompt}

    Evaluate the user's answer.
    """

    response = llm.invoke(final_prompt)

    return response.content