import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    from src.config.settings import settings
    api_key = settings.GOOGLE_API_KEY

genai.configure(api_key=api_key)

print("Models:")
try:
    for m in genai.list_models():
        if "gemini" in m.name:
            print(f"Name: {m.name} | Supported: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error: {e}")
