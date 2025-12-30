import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    print("--- Debug Gemini API (ASCII) ---")
    print(f"API Key present: {bool(api_key)}")
    
    if not api_key:
        print("[ERROR] GOOGLE_API_KEY not set.")
        return

    client = genai.Client(api_key=api_key)
    
    model_id = "gemini-1.5-flash"
    print(f"Testing Model: {model_id}")
    
    try:
        response = await client.aio.models.generate_content(
            model=model_id,
            contents="Hello, are you online?"
        )
        print(f"[SUCCESS] Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] API Call Failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
