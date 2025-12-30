import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)

class SafetyManager:
    """
    Enforces safety guardrails based on the application's SAFETY_MODE.
    """
    
    DESTRUCTIVE_ACTIONS = {
        "DELETE_FILE",
        "OVERWRITE_FILE", 
        "EXECUTE_COMMAND",
        "EXECUTE_BINARY"
    }

    @staticmethod
    def check_action(action_type: str, target: str) -> bool:
        """
        Checks if an action is permitted under current settings.
        
        Args:
            action_type: The type of action (e.g., "WRITE_FILE", "DELETE_FILE")
            target: The target resource (file path, command, etc.)
            
        Returns:
            bool: True if allowed, False if blocked (requires approval).
        """
        if not settings.SAFETY_MODE:
            # If safety mode is OFF (Autonomy Level HIGH), allow everything (but log it)
            logger.info(f"SAFETY_MODE=False. Allowing destructive action: {action_type} on {target}")
            return True

        if action_type in SafetyManager.DESTRUCTIVE_ACTIONS:
            logger.warning(f"SAFETY ALERT: Blocked destructive action '{action_type}' on '{target}' because SAFETY_MODE is ON.")
            return False
            
        return True

    @staticmethod
    def approve_action(action_type: str, target: str) -> bool:
        """
        Simulates a human-in-the-loop approval mechanism.
        For now, this just logs and returns False as we don't have a real UI callback yet.
        """
        logger.info(f"Requesting approval for: {action_type} on {target}")
        # In a real system, this would trigger a UI prompt or wait for API signal.
        return False
