import asyncio
import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def test_model(client, model_name, f):
    msg = f"\n--- Testing {model_name} ---"
    print(msg)
    f.write(msg + "\n")
    try:
        response = await client.aio.models.generate_content(
            model=model_name,
            contents="Hello",
            config={"response_mime_type": "application/json"}
        )
        msg = f"[OK] SUCCESS: {response.text}"
        print(msg)
        f.write(msg + "\n")
        return True
    except Exception as e:
        msg = f"[FAIL] ERROR: {e}"
        print(msg)
        f.write(msg + "\n")
        return False

async def main():
    with open("debug_error.log", "w", encoding="utf-8") as f:
        # Check SDK Version
        try:
            import importlib.metadata
            ver = importlib.metadata.version("google-genai")
            f.write(f"SDK Version: {ver}\n")
            print(f"SDK Version: {ver}")
        except:
            f.write("SDK Version: Unknown\n")
            print("SDK Version: Unknown")

        api_key = os.getenv("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)

        models_to_test = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-001",
            "gemini-1.5-pro",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
        ]

        working_model = None
        for model in models_to_test:
            if await test_model(client, model, f):
                working_model = model
                break
        
        if working_model:
            print(f"\nRECOMMENDATION: Use '{working_model}'")
        else:
            print("\nALL MODELS FAILED.")

if __name__ == "__main__":
    asyncio.run(main())
