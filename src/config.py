"""
Shared Configuration for Project Aether.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secrets (Safe for Git)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    # Fallback/Warning (Optional)
    print("WARNING: GROQ_API_KEY not found in .env. System may fail.")

MEMORY_FILE = "memory.json"
