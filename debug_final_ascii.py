import asyncio
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def test_model(client, model_name):
    print(f"\n--- Testing {model_name} ---")
    try:
        response = await client.aio.models.generate_content(
            model=model_name,
            contents="Hello",
            config={"response_mime_type": "application/json"}
        )
        print(f"[OK] SUCCESS: {response.text}")
        return True
    except Exception as e:
        print(f"[FAIL] ERROR: {e}")
        return False

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash",
    ]

    working_model = None
    for model in models_to_test:
        if await test_model(client, model):
            working_model = model
            break
    
    if working_model:
        print(f"\nRECOMMENDATION: Use '{working_model}'")
    else:
        print("\nALL MODELS FAILED.")

if __name__ == "__main__":
    asyncio.run(main())
