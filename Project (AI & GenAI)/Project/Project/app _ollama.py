import streamlit as st
import tempfile
import os
from datetime import datetime

from modules.extract import extract_text_from_pdf
from modules.chunk import split_text
from modules.embed_store import embed_and_store
from modules.rag_answer import summarize_report, answer_question_with_context

st.set_page_config(page_title="Medical Report Analyzer", layout="wide")
st.title("📄 Medical Report Analyzer (with Chat)")

uploaded_file = st.file_uploader("📤 Upload your medical report (PDF)", type=["pdf"])

if uploaded_file:
    # Save PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Extract and chunk
    raw_text = extract_text_from_pdf(tmp_path)
    chunks = split_text(raw_text)
    index, embed_model, stored_chunks = embed_and_store(chunks)
    st.session_state.stored_chunks = stored_chunks
    st.session_state.embed_model = embed_model
    st.session_state.index = index

    # Summarize
    with st.spinner("Generating summary..."):
        summary = summarize_report(stored_chunks)

    st.subheader("📝 Report Summary")
    st.markdown(summary)

    # Save summary
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = "summaries"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"summary_{timestamp}.txt")
    with open(file_path, "w") as f:
        f.write(summary)

    with open(file_path, "rb") as f:
        st.download_button("⬇️ Download Summary", data=f, file_name=os.path.basename(file_path), mime="text/plain")

    # Analyze another
    if st.button("🔄 Analyze Another Report"):
        st.session_state.clear()
        st.experimental_rerun()

    # 💬 Chatbot section
    st.markdown("### 💬 Ask questions about your report or general health")

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    for msg in st.session_state.conversation_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a question...")

    if user_query:
        st.session_state.conversation_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context_chunks = st.session_state.get("stored_chunks", [])
                index = st.session_state.get("index", None)
                model = st.session_state.get("embed_model", None)

                response = answer_question_with_context(
                    query=user_query,
                    chunks=context_chunks,
                    index=index,
                    model=model,
                    top_k=3
                )

                st.markdown(response)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})
