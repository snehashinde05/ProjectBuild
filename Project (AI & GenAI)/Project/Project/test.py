import google.generativeai as genai
print("hello sanskriti")
genai.configure(api_key="AIzaSyDEQokgWPkgqA5WKNXZPMYxhsVaDC-NTkk")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello!")
print(response.text)