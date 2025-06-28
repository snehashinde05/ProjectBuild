import google.generativeai as genai
print("hello sanskriti")
genai.configure(api_key="your_api_key_here")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello!")
print(response.text)