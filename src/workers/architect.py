import os
import subprocess
import logging
from pathlib import Path
from src.workers.base import BaseAgent
from src.models.artifacts import ActionArtifact
from src.utils.safety import SafetyManager

logger = logging.getLogger(__name__)

class Architect(BaseAgent):
    """
    The Architect: Responsible for File I/O and Code Execution.
    """
    def __init__(self):
        super().__init__(agent_id="ARCHITECT_001")

    async def execute(self, step_data: dict) -> ActionArtifact:
        """
        Executes file/code operations.
        """
        action = step_data.get("action", "").upper()
        # For EXECUTE, the target is the 'command'. For others, it's 'path'.
        target = step_data.get("path", "")
        if action == "EXECUTE" and not target:
            target = step_data.get("command", "")
        
        content = step_data.get("content", "")
        
        input_params = {"action": action, "path": target, "content_preview": content[:100] if content else None}

        if not action or not target:
            return self._create_artifact("UNKNOWN", input_params, "FAILED: Missing action or path")

        # Map to tool names
        if action == "WRITE":
            tool = "WRITE_FILE"
            if os.path.exists(target): tool = "OVERWRITE_FILE"
        elif action == "DELETE":
            tool = "DELETE_FILE"
        elif action == "EXECUTE":
            tool = "EXECUTE_COMMAND"
        elif action == "READ":
            tool = "READ_FILE"
        else:
            tool = "UNKNOWN"

        # Check Safety
        if not SafetyManager.check_action(tool, target):
            return self._create_artifact(tool, input_params, "FAILED: Action blocked by SafetyManager")

        try:
            if action == "WRITE":
                result = self._write_file(target, content)
            elif action == "READ":
                result = self._read_file(target)
            elif action == "DELETE":
                result = self._delete_file(target)
            elif action == "EXECUTE":
                result = self._execute_command(target)
            else:
                result = f"FAILED: Unsupported action: {action}"
                
            return self._create_artifact(tool, input_params, result)
            
        except Exception as e:
            logger.error(f"Error in Architect execution: {e}")
            return self._create_artifact(tool, input_params, f"FAILED: {str(e)}")

    def _write_file(self, path: str, content: str) -> str:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"SUCCESS: File written. Size: {len(content)} bytes"

    def _read_file(self, path: str) -> str:
        if not os.path.exists(path):
            return "FAILED: File not found"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"SUCCESS: Read {len(content)} bytes"

    def _delete_file(self, path: str) -> str:
        if not os.path.exists(path):
            return "FAILED: File not found"
        os.remove(path)
        return "SUCCESS: File deleted"

    def _execute_command(self, command: str) -> str:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"SUCCESS: {result.stdout}"
        else:
            return f"FAILED: {result.stderr}"
