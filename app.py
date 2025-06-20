import streamlit as st
import os
from src.summary import summary_pdf
from src.Document_handler import doc_handler
from src.ask_anything import ask_anything
from src.challenge_me import generate_quiz, evaluate_answer

# --- Page config ---
st.set_page_config(page_title="AI Assistant For Your Document", layout="centered")

# --- Init session state ---
if "processed" not in st.session_state:
    st.session_state["processed"] = False
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = ""
if "quiz_context" not in st.session_state:
    st.session_state["quiz_context"] = ""

# --- Title ---
st.title("🤖 AI Assistant For Your Document")

# --- Sidebar: Upload ---
with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    process_btn = st.button("🚀 Process Document")

# --- Process document ---
if process_btn:
    if uploaded_file is not None:
        os.makedirs("uploads", exist_ok=True)
        for file in os.listdir("uploads"):
            os.remove(os.path.join("uploads", file))

        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("⏳ Processing document..."):
            doc_handler()

        st.success("✅ Document processed successfully! You can now use AI assistant.")
        st.sidebar.success(f"Uploaded: {uploaded_file.name}")

        st.session_state["processed"] = True
        st.session_state["messages"] = []
        st.session_state["quiz_questions"] = ""
        st.session_state["quiz_context"] = ""

    else:
        st.error("⚠️ Please upload a file first!")

# --- Main App ---
if st.session_state["processed"]:
    st.header("⚙️ Choose Action")

    option = st.radio("Select Action:", ["📜 Generate Summary", "💬 Ask Anything", "🎯 Challenge Me"])

    # --- Generate Summary ---
    if option == "📜 Generate Summary":
        st.subheader("📜 Document Summary")
        if st.button("📝 Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = summary_pdf()
            st.success("✅ Summary Generated!")
            st.write(summary)

    # --- Ask Anything ---
    elif option == "💬 Ask Anything":
        st.subheader("💬 Chat with Your Document")

        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_question = st.chat_input("Ask a question about the document...")

        if user_question:
            st.session_state["messages"].append({"role": "user", "content": user_question})

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.spinner("💭 Thinking..."):
                answer = ask_anything(user_question)

            st.session_state["messages"].append({"role": "assistant", "content": answer})

            with st.chat_message("assistant"):
                st.markdown(answer)

    # --- Challenge Me ---
    elif option == "🎯 Challenge Me":
        st.subheader("🎯 Challenge Yourself!")

        if st.button("🎲 Generate Quiz"):
            with st.spinner("Generating quiz..."):
                quiz, context = generate_quiz()
            st.session_state["quiz_questions"] = quiz
            st.session_state["quiz_context"] = context
            st.success("✅ Quiz Ready!")
            st.markdown("### 📝 Quiz Questions:")
            st.write(quiz)

        if st.session_state["quiz_questions"]:
            st.subheader("✏️ Your Answer")
            user_answer = st.text_area("Type your answer here:")

            if st.button("📤 Submit Answer"):
                with st.spinner("Evaluating your answer..."):
                    feedback = evaluate_answer(user_answer, st.session_state["quiz_context"])
                st.markdown("### 🏆 Result:")
                st.write(feedback)

else:
    st.info("⬅️ Please upload and process a document first.")
