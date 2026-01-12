"""
Memory Persistence Module.
Handles loading/saving to memory.json.
"""
import os
import json
from .config import MEMORY_FILE

def load_memory():
    """Load memory from file or return empty dict."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_memory(key, value):
    """Update memory and save to file."""
    mem = load_memory()
    mem[key] = value
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(mem, f, indent=2)
        return f"SUCCESS: Remembered '{key}' = '{value}'"
    except Exception as e:
        return f"ERROR: Could not save memory. {str(e)}"
