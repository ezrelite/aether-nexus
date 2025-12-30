from abc import ABC, abstractmethod
import logging
import hashlib
from typing import Any, Dict
from src.models.artifacts import ActionArtifact

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Abstract Base Class for all Workers.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    async def execute(self, step_data: dict) -> ActionArtifact:
        """
        Executes a specific step delegated by the Nexus.
        
        Args:
            step_data: Dictionary containing instructions and parameters.
            
        Returns:
            ActionArtifact: The result of the action.
        """
        pass

    def _create_artifact(
        self, 
        tool_used: str, 
        input_params: Dict[str, Any], 
        output_result: str
    ) -> ActionArtifact:
        """
        Helper to create a standardized ActionArtifact.
        Computes a simple verification hash.
        """
        artifact = ActionArtifact(
            agent_id=self.agent_id,
            tool_used=tool_used,
            input_params=input_params,
            output_result=output_result
        )
        
        # Compute Hash (AgentID + Tool + Output + Timestamp)
        data_to_hash = f"{artifact.agent_id}:{artifact.tool_used}:{artifact.output_result}:{artifact.timestamp.isoformat()}"
        artifact.verification_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        return artifact
