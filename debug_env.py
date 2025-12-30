import os
from dotenv import load_dotenv

print("--- Environment Diagnostic ---")
print(f"CWD: {os.getcwd()}")
print(f"Loading .env...")
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
if key:
    print(f"GOOGLE_API_KEY found: {key[:5]}...{key[-5:] if len(key)>10 else ''}")
else:
    print("GOOGLE_API_KEY NOT found in os.environ")

try:
    from src.config.settings import settings
    print(f"\nSettings.GOOGLE_API_KEY: {settings.GOOGLE_API_KEY[:5] if settings.GOOGLE_API_KEY else 'None'}...")
except Exception as e:
    print(f"Error loading settings: {e}")
