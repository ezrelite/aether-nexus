import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Test 1
    print("Testing 'gemini-1.5-flash'...")
    try:
        response = await client.aio.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Hi"
        )
        print(f"[SUCCESS] {response.text}")
    except Exception as e:
        print(f"[FAIL] {e}")

    # Test 2
    print("\nTesting 'gemini-2.0-flash-exp'...")
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-exp", 
            contents="Hi"
        )
        print(f"[SUCCESS] {response.text}")
    except Exception as e:
        print(f"[FAIL] {e}")

if __name__ == "__main__":
    asyncio.run(main())
