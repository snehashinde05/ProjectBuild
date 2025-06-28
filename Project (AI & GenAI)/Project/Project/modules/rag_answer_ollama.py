import requests

def run_local_llm(prompt, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    print("This is ollama")
    return response.json()["response"]

def summarize_report(chunks):
    full_context = "\n".join(chunks)
    prompt = f"""
You are a helpful and friendly medical assistant. A patient has uploaded the following medical report:

---
{full_context}
---

Please provide a simple summary in everyday language that covers:
1. Which parameters are normal.
2. Which are abnormal and what they might indicate.
3. Possible causes or concerns.
4. A gentle suggestion to consult a doctor.

Avoid jargon and keep the tone supportive.
"""
    return run_local_llm(prompt)
