from google.generativeai import GenerativeModel, configure
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

configure(api_key=GEMINI_API_KEY)

model = GenerativeModel('gemini-pro')
response = model.generate_content("Hello")
print(response.text)
