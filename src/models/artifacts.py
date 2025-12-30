from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class ActionArtifact(BaseModel):
    """
    Structured artifact representing an action taken by a worker.
    """
    agent_id: str = Field(..., description="ID of the agent performing the action")
    tool_used: str = Field(..., description="Name of the tool or action type executed")
    input_params: Dict[str, Any] = Field(..., description="Parameters passed to the tool")
    output_result: str = Field(..., description="Unstructured output or result of the action")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of action")
    verification_hash: Optional[str] = Field(None, description="Hash for verifying artifact integrity")
