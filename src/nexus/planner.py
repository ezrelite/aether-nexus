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

    async def generate_plan(self, intent: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generates a plan containing an assistant reply and execution steps.
        Returns:
            {
                "assistant_reply": str,
                "execution_plan": List[Dict]
            }
        """
        if not self.client:
            # Mock mode fallback
            logger.info("Generating MOCK plan (No API Key).")
            return {
                "assistant_reply": f"I'm operating in Mock Mode, but I'll simulate a plan to {intent}.",
                "execution_plan": [
                    {"worker": "ARCHITECT", "action": "WRITE", "path": "temp/hello_mock.txt", "content": "Hello from Mock Planner!"},
                    {"worker": "NAVIGATOR", "action": "SEARCH", "query": "Mock Search"},
                ]
            }

        # Construct System Prompt
        system_prompt = """
You are AETHER (Autonomous Executive Task & High-Efficiency Router).
You are a "Cognitive Operating Layer" capable of orchestrating a fleet of specialized AI workers.

### YOUR GOAL
Your objective is to receive a user intent ("{intent}"), analyze it, and generate a structured plan to execute it using your available tools.

### AVAILABLE WORKERS
1. [NAVIGATOR]: A web browsing agent. 
   - Capabilities: SEARCH (query), FETCH (url).
   - Use for: Research, news, fact-checking, summarizing websites.
2. [ARCHITECT]: A file system and engineering agent.
   - Capabilities: WRITE (path, content), READ (path), DELETE (path), EXECUTE (command).
   - Use for: Coding, saving reports, data processing, file management.
3. [ANALYST]: A logic agent. 
   - Capabilities: ANALYZE.
   - Use for: Synthesizing large data.

### OUTPUT PROTOCOL (CRITICAL)
You must ALWAYS output a valid JSON object. Do not output markdown blocks or conversational text outside the JSON.

The JSON must follow this exact schema:
{{
    "thought_process": "Internal monologue. Briefly analyze the request and the best strategy.",
    "assistant_reply": "A friendly, natural language response to the user. Explain what you are about to do (e.g., 'I will search for X and then save it to Y').",
    "execution_plan": [
        {{
            "worker": "NAVIGATOR",
            "action": "SEARCH",
            "query": "search query...",
            "rationale": "Need real-time data to answer the prompt."
        }},
        {{
            "worker": "ARCHITECT",
            "action": "WRITE",
            "path": "/path/to/file.md",
            "content": "File content here...",
            "rationale": "User requested a written report."
        }}
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
            
            # Log the cognitive process
            if "thought_process" in data:
                logger.info(f"🧠 AETHER Thoughts: {data['thought_process']}")
            
            if "execution_plan" not in data or "assistant_reply" not in data:
                 raise PlanningError("Response missing 'execution_plan' or 'assistant_reply' key.")
            
            return {
                "assistant_reply": data["assistant_reply"],
                "execution_plan": data["execution_plan"]
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parse Error: {e}")
            raise PlanningError(f"Failed to parse JSON plan: {e}")
        except Exception as e:
            logger.error(f"Gemini API Error after retries: {e}")
            logger.warning("⚠️  API Failed. Falling back to MOCK DEMO PLAN.")
            
            # Fallback Plan that demonstrates capabilities (Dynamic based on Intent)
            logger.warning(f"Returning Mock Plan for intent: {intent}")
            return {
                "assistant_reply": f"I'm encountering some interference with the API network, but I'll deploy a simulation to address your request: '{intent}'.",
                "execution_plan": [
                    {
                        "worker": "NAVIGATOR", 
                        "action": "SEARCH", 
                        "query": intent  # Use the user's actual intent
                    },
                    {
                        "worker": "ARCHITECT", 
                        "action": "WRITE", 
                        "path": "mission_report.md", 
                        "content": f"# Mission Report: {intent}\n\n(This is a generated mock summary as the AI Brain is currently rate-limited)\n\n## Analysis\nThe system has processed the request to '{intent}'.\n\n### Key Findings (Simulated):\n- Found 3 relevant sources.\n- Synthesized key data points.\n- Verified autonomy constraints."
                    },
                    {
                        "worker": "ARCHITECT",
                        "action": "EXECUTE",
                        "command": "dir" 
                    }
                ]
            }

planner = Planner()
