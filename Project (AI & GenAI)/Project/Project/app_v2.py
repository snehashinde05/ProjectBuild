import streamlit as st
from modules.extract import extract_text_from_pdf
from modules.chunk import split_text
from modules.embed_store import embed_and_store
from modules.rag_answer import summarize_report
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="Medical Report Summarizer (Ollama)", layout="centered")

st.title("🧠 Medical Report Summarizer (via Ollama)")
st.markdown("Upload a medical report PDF and get a plain-language summary using a local LLM.")

# Session state to manage workflow
if "summary_generated" not in st.session_state:
    st.session_state.summary_generated = False

# Reset function
def reset_app():
    st.session_state.summary_generated = False
    st.session_state.uploaded_file = None
    st.experimental_rerun()

# Upload PDF
if not st.session_state.summary_generated:
    uploaded_file = st.file_uploader("📄 Upload your medical report", type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        st.info("⏳ Processing report...")

        raw_text = extract_text_from_pdf(tmp_path)
        chunks = split_text(raw_text)
        index, model_embed, stored_chunks = embed_and_store(chunks)

        if st.button("🧾 Generate Summary"):
            with st.spinner("Running Mistral via Ollama..."):
                summary = summarize_report(stored_chunks)
                st.session_state.summary_generated = True
                st.session_state.summary_text = summary

# Display summary and save
if st.session_state.summary_generated:
    st.success("✅ Summary generated!")
    st.markdown("### 📋 Summary:")
    st.write(st.session_state.summary_text)

    # Save to file
    os.makedirs("summaries", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"summary_{timestamp}.txt"
    filepath = os.path.join("summaries", filename)
    with open(filepath, "w") as f:
        f.write(st.session_state.summary_text)

    # Download button
    with open(filepath, "rb") as f:
        st.download_button(
            label="⬇️ Download Summary",
            data=f,
            file_name=filename,
            mime="text/plain"
        )

    # Reset button
    st.markdown("---")
    st.button("🔄 Analyze Another Report", on_click=reset_app)
