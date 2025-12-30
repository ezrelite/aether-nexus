import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Test 1: explicit models/ prefix
    print("Testing 'models/gemini-1.5-flash'...")
    try:
        response = await client.aio.models.generate_content(
            model="models/gemini-1.5-flash", 
            contents="Hi"
        )
        print(f"✅ Success with prefix: {response.text}")
    except Exception as e:
        print(f"❌ Failed with prefix: {e}")

    # Test 2: no prefix
    print("\nTesting 'gemini-1.5-flash'...")
    try:
        response = await client.aio.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Hi"
        )
        print(f"✅ Success without prefix: {response.text}")
    except Exception as e:
        print(f"❌ Failed without prefix: {e}")
        
    # Test 3: gemini-1.5-flash-002
    print("\nTesting 'gemini-1.5-flash-002'...")
    try:
        response = await client.aio.models.generate_content(
            model="gemini-1.5-flash-002", 
            contents="Hi"
        )
        print(f"✅ Success 002: {response.text}")
    except Exception as e:
        print(f"❌ Failed 002: {e}")

if __name__ == "__main__":
    asyncio.run(main())
