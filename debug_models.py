import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    print("--- Listing Gemini Models ---")
    
    client = genai.Client(api_key=api_key)
    
    try:
        # According to standard async patterns, await the method call
        models = await client.aio.models.list()
        for model in models:
            print(f"- {model.name} (Display: {model.display_name})")
            
    except Exception as e:
        print(f"[ERROR] List Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
