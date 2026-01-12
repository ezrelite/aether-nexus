import google.generativeai as genai
import os
import json
import hashlib
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from google.api_core.exceptions import ResourceExhausted
from src.config.settings import settings

logger = logging.getLogger(__name__)

# 1. Setup
api_key = os.getenv("GOOGLE_API_KEY") or settings.GOOGLE_API_KEY
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.warning("GOOGLE_API_KEY not found. Operations may fail.")

# 2. The Standard Model
# Using 'gemini-pro-latest' as 'gemini-pro' is deprecated/renamed
try:
    model = genai.GenerativeModel('gemini-pro-latest')
except Exception as e:
    logger.error(f"Error initializing model: {e}")
    model = None

# CACHE SETUP
CACHE_FILE = "response_cache.json"
if not os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'w') as f: json.dump({}, f)
    except Exception:
        pass # Handle permission errors gracefully-ish

def get_cache_key(text):
    return hashlib.md5(text.encode()).hexdigest()

SYSTEM_PROMPT = """
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
"""

# THE SMART RETRY LOGIC
# If we hit a limit, we wait 2s, then 4s, then 8s... up to 60s
@retry(
    retry=retry_if_exception_type(ResourceExhausted),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=10, max=120),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def call_gemini_safe(prompt):
    if not model:
        raise Exception("Model not initialized.")
    response = model.generate_content(prompt)
    return response.text

def generate_plan_sync(user_input):
    # 1. CHECK CACHE FIRST (Save API calls)
    cache_key = get_cache_key(user_input)
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f: cache = json.load(f)
            if cache_key in cache:
                logger.info("⚡ Using Cached Response (Zero API Cost)")
                return cache[cache_key]
    except Exception as e:
        logger.warning(f"Cache Read Error: {e}")

    # 2. CALL GOOGLE (With Retry Safety)
    try:
        full_prompt = f"{SYSTEM_PROMPT.format(intent=user_input)}\nUSER INTENT: {user_input}"
        plan_text = call_gemini_safe(full_prompt)
        
        # 3. SAVE TO CACHE
        try:
            current_cache = {}
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r') as f:
                    try:
                        current_cache = json.load(f)
                    except json.JSONDecodeError:
                        current_cache = {}
            
            current_cache[cache_key] = plan_text
            with open(CACHE_FILE, 'w') as f: json.dump(current_cache, f)
        except Exception as e:
             logger.warning(f"Cache Write Error: {e}")
        
        return plan_text
        
    except Exception as e:
        logger.error(f"Generative API Error: {e}")
        return json.dumps({
            "assistant_reply": f"I am overloaded. Please wait 1 minute. (Error: {str(e)})", 
            "execution_plan": []
        })

class Planner:
    """
    Wrapper for the legacy functional API to maintain compatibility with NexusEngine.
    """

    async def generate_plan(self, intent: str, history=None):
        logger.info(f"Generating plan via Legacy API (Robust) for: {intent}")
        import asyncio
        loop = asyncio.get_running_loop()
        # Offload sync work to thread to prevent blocking the event loop
        raw_json = await loop.run_in_executor(None, generate_plan_sync, intent)
        try:
            # Clean possible markdown formatting ```json ... ```
            clean_json = raw_json.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:]
            if clean_json.startswith("```"):
                clean_json = clean_json[3:]
            if clean_json.endswith("```"):
                clean_json = clean_json[:-3]
            
            return json.loads(clean_json)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from Legacy API response.")
            return {
                "assistant_reply": "I encountered an error processing the plan.",
                "execution_plan": []
            }

planner = Planner()
