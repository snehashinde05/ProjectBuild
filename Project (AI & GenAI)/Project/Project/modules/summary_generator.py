import fitz  # PyMuPDF
from modules.rag_answer import summarize_report

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_chars=3000):
    # Simple fixed-size chunking
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def generate_summary_from_pdf(uploaded_file):
    full_text = extract_text_from_pdf(uploaded_file)
    chunks = chunk_text(full_text)
    return summarize_report(chunks)
