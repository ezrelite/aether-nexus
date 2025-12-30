import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

print("Testing Imports...")
try:
    from src.config import settings
    print("Config: OK")
    from src.models import api, artifacts
    print("Models: OK")
    from src.utils import safety
    print("Utils: OK")
    from src.memory import cortex
    print("Memory: OK")
    from src.workers import base, architect, navigator, analyst
    print("Workers: OK")
    from src.nexus import planner, engine
    print("Nexus: OK")
    from src import main
    print("Main: OK")
    print("ALL MODULES IMPORTED SUCCESSFULLY")
except Exception as e:
    print(f"IMPORT FAILED: {e}")
    sys.exit(1)
