import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"--- Debug Gemini API ---")
    print(f"API Key present: {bool(api_key)}")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not set.")
        return

    client = genai.Client(api_key=api_key)
    
    model_id = "gemini-1.5-flash"
    print(f"Testing Model: {model_id}")
    
    try:
        response = await client.aio.models.generate_content(
            model=model_id,
            contents="Hello, are you online?"
        )
        print(f"✅ Success! Response: {response.text}")
    except Exception as e:
        print(f"❌ API Call Failed: {type(e).__name__}: {e}")
        # Try listing models to see if we have access/auth is generally working
        print("\nAttempting to list models...")
        try:
            # Note: client.models.list is synchronous or async depending on usage, 
            # but usually for listing we can try the async variant if available or sync.
             # SDK 0.1+ pattern varies, safe bet is usually just catching the error.
            pass 
        except Exception as list_e:
            print(f"Could not list models: {list_e}")

if __name__ == "__main__":
    asyncio.run(main())
