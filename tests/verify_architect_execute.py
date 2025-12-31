import asyncio
import sys
import os
sys.path.append(os.getcwd())
from src.workers.architect import Architect

async def test_architect_execute():
    print("--- Verifying Architect EXECUTE Action ---")
    architect = Architect()
    
    # Test Case: Action with 'command' parameter (Simulating Nexus Plan)
    step_data = {
        "worker": "ARCHITECT",
        "action": "EXECUTE",
        "command": "dir" # This caused failure before because 'path' was missing
    }
    
    print(f"Input: {step_data}")
    
    result = await architect.execute(step_data)
    
    print("\nResult Artifact:")
    print(f"Tool: {result.tool_used}")
    print(f"Output: {result.output_result[:100]}...")
    
    if "SUCCESS" in result.output_result:
        print("\n[OK] Verification PASSED: Architect successfully executed command.")
    elif "Action blocked by SafetyManager" in result.output_result:
        print("\n[OK] Verification PASSED: Parameters parsed correctly (Blocked by Safety).")
        # This confirms the `command` -> `target` logic worked, because otherwise it would happen BEFORE safety check.
    else:
        print("\n[FAIL] Verification FAILED: Architect did not execute command.")

if __name__ == "__main__":
    asyncio.run(test_architect_execute())
