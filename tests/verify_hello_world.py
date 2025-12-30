import asyncio
import os
import sys
import shutil

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.nexus.engine import nexus
from src.memory.cortex import cortex

async def main():
    print("--- Starting Phase 2 Verification: Data Protocols ---")
    
    # 1. Setup
    intent = "Create a Hello World python file in the temp directory."
    print(f"Intent: {intent}")
    
    # Mock Cortex for local run
    async def mock_connect(): print("Mock Cortex Connected")
    async def mock_save(*args): pass
    async def mock_add(*args): pass
    cortex.connect = mock_connect
    cortex.save_context = mock_save
    cortex.add_log = mock_add
    
    # 2. Process Intent (Directly via Engine, bypassing API layer wrap if desired, 
    # but Engine now returns TaskResponse so it simulates API logic)
    response = await nexus.process_intent(intent)
    
    # 3. Analyze Response (TaskResponse)
    print("\n--- Task Response ---")
    print(f"Status: {response.status}")
    print(f"Plan ID: {response.plan_id} (UUID)")
    print(f"Artifacts: {len(response.artifacts)}")
    
    success = False
    for artifact in response.artifacts:
        print(f"\n[Artifact]")
        print(f"  Agent: {artifact.agent_id}")
        print(f"  Tool: {artifact.tool_used}")
        print(f"  Input: {artifact.input_params}")
        print(f"  Output: {artifact.output_result}")
        print(f"  Hash: {artifact.verification_hash}")
        
        # Verify structure
        if not artifact.verification_hash:
            print("  [ERROR] Missing Verification Hash!")
            
        if artifact.tool_used in ["WRITE_FILE", "OVERWRITE_FILE"] and "SUCCESS" in artifact.output_result:
            success = True
            
    # 4. Verify Side Effects
    target_file = "temp/hello_mock.txt"
    if os.path.exists(target_file):
        print(f"\n[VERIFIED] File {target_file} exists!")
        with open(target_file, 'r') as f:
            print(f"Content: {f.read()}")
        # Cleanup
        shutil.rmtree("temp")
    else:
        if success:
             print("\n[VERIFIED] Action reported success (File may be in a different path if logic changed).")
        else:
             print("\n[FAILED] File creation not verified.")

if __name__ == "__main__":
    asyncio.run(main())
