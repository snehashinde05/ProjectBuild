import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key="your_api-key_here")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_diet_from_summary_ai(summary_text):
    prompt = f"""
You are a certified clinical dietitian.

A patient provided the following medical summary:

---
{summary_text}
---

Based on the following medical summary, create a personalized nutritional diet chart in **Markdown table format**.

Instructions:

- Use a **table** with 3 columns: Meal Time, Recommended Foods, Purpose.
- Format the foods and purposes using **bullet points (`•`)** with **line breaks (`<br>`)** inside each cell.
- The chart should include: Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner.
- Make it compatible with **Streamlit Markdown rendering**.
- Add **brief, practical, and locally relevant items**.
- Follow the dietary needs for conditions like anemia and slightly elevated cholesterol.
- Ensure the diet is **simple, practical, and culturally appropriate** for an Indian audience.

"""

    response = model.generate_content(prompt)
    return response.text
