import requests

def run_local_llm(prompt, model="mistral"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        print("Hi this is ollama")
        return response.json()["response"]
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"

# ✅ Summarize full report
def summarize_report(chunks):
    full_context = "\n".join(chunks)
    prompt = f"""
You are a helpful and friendly medical assistant. A patient has uploaded the following medical report:

---
{full_context}
---

Please provide a summary in plain, simple language:
1. Which results are normal.
2. Which are abnormal and what they might indicate.
3. Any health risks or concerns.
4. A gentle suggestion to consult a doctor.

Avoid technical jargon. Keep the tone warm and clear.
"""
    return run_local_llm(prompt)

# ✅ RAG-style question answering
def answer_question_with_context(query, chunks, index, model, top_k=3):
    if not chunks or not index or not model:
        return "⚠️ Report data not available. Please upload a medical report first."

    try:
        q_embed = model.encode([query])
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

        return run_local_llm(prompt)

    except Exception as e:
        return f"⚠️ Failed to generate answer: {str(e)}"
