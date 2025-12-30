import pytest
import asyncio
import json
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.nexus.planner import planner, PlanningError

# Sample valid JSON response from Gemini
SAMPLE_JSON_RESPONSE = """
{
  "reasoning": "I will create a file using the Architect.",
  "steps": [
     {"worker": "Architect", "action": "WRITE", "path": "test.txt", "content": "Hello"}
  ]
}
"""

@pytest.mark.asyncio
async def test_generate_plan_success():
    # Mock the GenerativeModel.generate_content_async method
    
    # We need to mock the model instance inside the planner.
    # Since planner instantiates it in __init__, we can replace it.
    
    mock_response = MagicMock()
    mock_response.text = SAMPLE_JSON_RESPONSE
    
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = mock_response
    
    # Inject mock
    original_model = planner.model
    planner.model = mock_model
    
    try:
        steps = await planner.generate_plan("Make a file")
        
        assert len(steps) == 1
        assert steps[0]["worker"] == "Architect"
        assert steps[0]["action"] == "WRITE"
        assert steps[0]["content"] == "Hello"
        
    finally:
        # Restore (though verify_hello_world uses logic that might rely on this, 
        # usually tests run in isolation or containers).
        planner.model = original_model

@pytest.mark.asyncio
async def test_generate_plan_invalid_json():
    mock_response = MagicMock()
    mock_response.text = "This is not JSON"
    
    mock_model = AsyncMock()
    mock_model.generate_content_async.return_value = mock_response
    
    original_model = planner.model
    planner.model = mock_model
    
    with pytest.raises(PlanningError):
        await planner.generate_plan("Make a file")
        
    planner.model = original_model

if __name__ == "__main__":
    # Allow running this script directly for manual verify
    try:
        asyncio.run(test_generate_plan_success())
        print("test_generate_plan_success: PASSED")
        asyncio.run(test_generate_plan_invalid_json())
        print("test_generate_plan_invalid_json: PASSED")
    except Exception as e:
        print(f"FAILED: {e}")
