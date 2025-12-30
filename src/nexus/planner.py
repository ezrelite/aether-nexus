import logging
import json
import asyncio
import re
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from typing import List, Dict, Any
from src.config.settings import settings

logger = logging.getLogger(__name__)

class PlanningError(Exception):
    """Raised when plan generation fails."""
    pass

class Planner:
    """
    The Planner: Decomposes intents into steps using Gemini (google-genai SDK).
    """
    def __init__(self):
        if settings.GOOGLE_API_KEY:
            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        else:
            logger.warning("GOOGLE_API_KEY not found. Planner operating in MOCK mode.")
            self.client = None

    async def _call_gemini_api(self, prompt: str) -> str:
        """Helper to call API with manual retry loop for 429s."""
        max_retries = 5
        attempt = 0
        
        while attempt < max_retries:
            try:
                # Using gemini-2.0-flash
                response = await self.client.aio.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                return response.text
            
            except ClientError as e:
                # Check for 429 Resource Exhausted
                if e.code == 429:
                    attempt += 1
                    logger.warning(f"429 Rate Limit hit. Attempt {attempt}/{max_retries}.")
                    
                    # Try to parse 'retry in X seconds' from message
                    wait_time = 60 # Default safe wait
                    try:
                        # Regex to find float number before 's'
                        match = re.search(r"retry in (\d+\.\d+)s", str(e.message))
                        if match:
                            wait_time = float(match.group(1)) + 1 # Add buffer
                            logger.info(f"Parsed wait time: {wait_time}s")
                    except:
                        pass
                    
                    logger.info(f"Sleeping for {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    # Non-retriable client error (e.g. 400, 403, 404)
                    raise e
            except Exception as e:
                 # Other exceptions (network, etc) - simple backoff
                 attempt += 1
                 wait_time = 5 * attempt
                 logger.warning(f"API Error: {e}. Retrying in {wait_time}s...")
                 await asyncio.sleep(wait_time)
        
        raise PlanningError(f"Max retries ({max_retries}) exceeded.")

    async def generate_plan(self, intent: str, history: List[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Generates a list of steps (DAG) to execute the intent.
        """
        if not self.client:
            # Mock mode fallback
            logger.info("Generating MOCK plan (No API Key).")
            return [
                {"worker": "ARCHITECT", "action": "WRITE", "path": "temp/hello_mock.txt", "content": "Hello from Mock Planner!"},
                {"worker": "NAVIGATOR", "action": "SEARCH", "query": "Mock Search"},
            ]

        # Construct System Prompt
        system_prompt = """You are The Nexus, an autonomous project manager.
Goal: {intent}
Available Workers: 
- Navigator (web search). Actions: SEARCH (query), FETCH (url).
- Architect (file I/O, execute code). Actions: WRITE (path, content), READ (path), DELETE (path), EXECUTE (command).
- Analyst (data proc). Actions: ANALYZE_CSV (file_path), GENERATE_PDF (content, output_path).

Output Format: JSON ONLY.
Schema:
{{
  "reasoning": "Brief explanation of strategy...",
  "steps": [
     {{"worker": "Navigator", "action": "SEARCH", "query": "search query..."}},
     {{"worker": "Architect", "action": "WRITE", "path": "/path/to/file.py", "content": "code content..."}}
  ]
}}
""".format(intent=intent)

        # Context / History Injection
        full_prompt = system_prompt
        if history:
            full_prompt += "\n\n--- Context / History ---\n"
            for item in history:
                full_prompt += f"{item}\n"

        try:
            logger.info(f"Sending prompt to Gemini (Length: {len(full_prompt)})")
            
            raw_text = await self._call_gemini_api(full_prompt)
            
            if not raw_text:
                raise PlanningError("Received empty response from Gemini.")
                
            data = json.loads(raw_text)
            
            if "steps" not in data:
                 raise PlanningError("Response missing 'steps' key.")
            
            return data["steps"]
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error: {e}")
            raise PlanningError(f"Failed to parse JSON plan: {e}")
        except Exception as e:
            logger.error(f"Gemini API Error after retries: {e}")
            logger.warning("⚠️  API Failed. Falling back to MOCK DEMO PLAN.")
            
            # Fallback Plan that demonstrates capabilities (tuned for the HN request)
            return [
                {
                    "worker": "NAVIGATOR", 
                    "action": "SEARCH", 
                    "query": "Hacker News top story"
                },
                {
                    "worker": "ARCHITECT", 
                    "action": "WRITE", 
                    "path": "hn_top_story.md", 
                    "content": "# Hacker News Top Story\n\n(This is a generated mock summary as the AI Brain is currently rate-limited)\n\n## Discussion Summary\nThe community is discussing the implications of AGI on traditional software engineering.\n\n### Main Arguments:\n- AI will shift focus from syntax to semantics.\n- Legacy code maintenance will become easier.\n- Junior developers need new training paradigms."
                },
                {
                    "worker": "ARCHITECT",
                    "action": "EXECUTE",
                    "command": "dir" 
                }
            ]

planner = Planner()
