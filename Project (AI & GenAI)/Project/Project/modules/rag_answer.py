import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
# Use environment variable or hardcoded API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key="AIzaSyAo4jpFEz4nWvQVhD5XkmZEVjKvAWQI064")

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


# ✅ Summarize medical report
def summarize_report(chunks):
    full_context = "\n".join(chunks)
    prompt = f"""
A patient has uploaded the following medical report:

---
{full_context}
---

You are a medical assistant tasked with summarizing the report **clearly and concisely**. 

Please return the summary in the following markdown structure:

---

✅ **Normal Results**
- [Test Name]: [Result Summary] — [Short Implication]

⚠️ **Abnormal Results**
- [Test Name]: [Result Summary] — [Concern or Diagnosis]

🧾 **Summary**
- [Brief overall interpretation in 2–4 bullet points]

👩‍⚕️ **Suggestion**
- [List actionable next steps or recommendations in bullet form]

Keep language **simple and friendly** for a person with no medical background. Use bullet points, avoid jargon, and be brief but clear.

Only return the formatted summary. Do not include explanations or extra commentary outside the structure.
"""
    response = model.generate_content(prompt)
    return response.text


# ✅ RAG-style Question Answering
def answer_question_with_context(query, chunks, index, model_embed, top_k=3):
    if not chunks or not index or not model_embed:
        return "⚠️ Report data not available. Please upload a medical report first."

    try:
        q_embed = model_embed.encode([query])
        D, I = index.search(q_embed, top_k)
        retrieved = "\n".join([chunks[i] for i in I[0]])

        prompt = f"""
A patient has uploaded a medical report. Use the context below to answer their question in simple, friendly language.

--- Report Context ---
{retrieved}

--- Question ---
{query}

--- Answer ---
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"⚠️ Failed to generate answer: {str(e)}"
