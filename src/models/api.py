from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
from uuid import UUID
from src.models.artifacts import ActionArtifact

class TaskRequest(BaseModel):
    """
    Request to execute a complex task.
    """
    intent: str = Field(..., description="The high-level goal or command")
    autonomy_level: Literal["high", "low"] = Field("high", description="Level of autonomy permitted")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context (files, search results, etc.)")

class TaskResponse(BaseModel):
    """
    Response containing the execution results.
    """
    status: str = Field(..., description="Overall status (e.g., COMPLETED, FAILED)")
    plan_id: UUID = Field(..., description="Unique Identifier for the generated plan")
    artifacts: List[ActionArtifact] = Field(default_factory=list, description="List of actions taken")
