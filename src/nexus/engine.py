import logging
import uuid
import uuid as uuid_lib
from typing import List, Dict, Any
from src.nexus.planner import planner
from src.workers.architect import Architect
from src.workers.navigator import Navigator
from src.workers.analyst import Analyst
from src.memory.cortex import cortex
from src.models.api import TaskResponse
from src.models.artifacts import ActionArtifact

logger = logging.getLogger(__name__)

class NexusEngine:
    """
    The Nexus Engine: Orchestrates the work.
    """
    def __init__(self):
        # Pre-instantiate workers or instantiate on demand.
        # Doing pre-instantiation for simplicity and caching if needed.
        self.workers = {
            "ARCHITECT": Architect(),
            "NAVIGATOR": Navigator(),
            "ANALYST": Analyst()
        }

    async def run(self, intent: str, session_id: str = None) -> TaskResponse:
        """
        Main entry point for processing user intent.
        Executes the Grand Unification loop: Plan -> Dispatch -> Aggregate.
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            
        plan_id = uuid_lib.uuid4()
            
        logger.info(f"Nexus Running Intent: {intent} [Session: {session_id}]")
        
        # 1. Save Intent to Context
        await cortex.save_context(session_id, "last_intent", intent)
        
        # 2. Generate Plan
        try:
            logger.info("Generating Plan...")
            plan_steps = await planner.generate_plan(intent)
            logger.info(f"Plan Generated with {len(plan_steps)} steps.")
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return TaskResponse(
                status="FAILED",
                plan_id=plan_id,
                artifacts=[
                    ActionArtifact(
                        agent_id="NEXUS_PLANNER",
                        tool_used="PLANNING",
                        input_params={"intent": intent},
                        output_result=f"Plan generation failed: {str(e)}"
                    )
                ]
            )

        artifacts: List[ActionArtifact] = []
        
        # 3. Execution Loop
        for i, step in enumerate(plan_steps):
            worker_name_raw = step.get("worker", "UNKNOWN")
            worker_name = worker_name_raw.upper()
            
            logger.info(f"Executing Step {i+1}/{len(plan_steps)}: {worker_name} -> {step.get('action')}")
            
            worker = self.workers.get(worker_name)
            
            if worker:
                try:
                    artifact = await worker.execute(step)
                    artifacts.append(artifact)
                    
                    # Log to Cortex
                    await cortex.add_log(session_id, artifact.model_dump(mode='json'))
                    
                except Exception as e:
                    logger.error(f"Worker {worker_name} failed: {e}")
                    # Create a failure artifact
                    error_artifact = ActionArtifact(
                         agent_id=worker_name,
                         tool_used=step.get("action", "UNKNOWN"),
                         input_params=step,
                         output_result=f"Exception during execution: {str(e)}"
                    )
                    artifacts.append(error_artifact)
            else:
                logger.warning(f"Unknown worker: {worker_name_raw}")
                error_artifact = ActionArtifact(
                     agent_id="NEXUS_ENGINE",
                     tool_used="DISPATCH",
                     input_params=step,
                     output_result=f"Unknown worker type: {worker_name_raw}"
                )
                artifacts.append(error_artifact)
                
        # 4. Generate Final Status
        # Simple heuristic: if any failure in artifacts, mark as partial or failed.
        failure_count = sum(1 for a in artifacts if "FAILED" in a.output_result or "Exception" in a.output_result)
        
        if failure_count == 0 and len(artifacts) > 0:
            status = "COMPLETED"
        elif failure_count < len(artifacts):
            status = "PARTIAL_FAILURE"
        else:
            status = "FAILED"
        
        logger.info(f"Execution Finished. Status: {status}")
        
        return TaskResponse(
            status=status,
            plan_id=plan_id,
            artifacts=artifacts
        )

# Global Instance
nexus = NexusEngine()
