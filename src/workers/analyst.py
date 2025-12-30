import logging
import pandas as pd
from reportlab.pdfgen import canvas
from src.workers.base import BaseAgent
from src.models.artifacts import ActionArtifact

logger = logging.getLogger(__name__)

class Analyst(BaseAgent):
    """
    The Analyst: Responsible for Data Processing and Reporting.
    """
    def __init__(self):
        super().__init__(agent_id="ANALYST_001")

    async def execute(self, step_data: dict) -> ActionArtifact:
        """
        Executes data/reporting tasks.
        """
        action = step_data.get("action", "").upper()
        file_path = step_data.get("file_path")
        output_path = step_data.get("output_path")
        
        input_params = step_data.copy()
        
        try:
            if action == "ANALYZE_CSV":
                if not file_path:
                    return self._create_artifact("ANALYZE_CSV", input_params, "FAILED: Missing file_path")
                return self._analyze_csv(file_path, input_params)
            
            elif action == "GENERATE_PDF":
                content = step_data.get("content")
                if not content or not output_path:
                    return self._create_artifact("GENERATE_PDF", input_params, "FAILED: Missing content or output_path")
                return self._generate_pdf(content, output_path, input_params)
                
            else:
                return self._create_artifact("UNKNOWN", input_params, f"FAILED: Unsupported action: {action}")
        except Exception as e:
            logger.error(f"Error in Analyst execution: {e}")
            return self._create_artifact(action, input_params, f"FAILED: {str(e)}")

    def _analyze_csv(self, file_path: str, input_params: dict) -> ActionArtifact:
        try:
            df = pd.read_csv(file_path)
            result = f"SUCCESS: Analyzed {len(df)} rows. Columns: {list(df.columns)}"
            return self._create_artifact("ANALYZE_CSV", input_params, result)
        except Exception as e:
            return self._create_artifact("ANALYZE_CSV", input_params, f"FAILED: {str(e)}")

    def _generate_pdf(self, content: str, output_path: str, input_params: dict) -> ActionArtifact:
        try:
            c = canvas.Canvas(output_path)
            c.drawString(100, 750, "AETHER Analyst Report")
            y = 700
            for line in content.split('\n'):
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, line)
                y -= 20
            c.save()
            return self._create_artifact("GENERATE_PDF", input_params, f"SUCCESS: PDF Generated at {output_path}")
        except Exception as e:
            return self._create_artifact("GENERATE_PDF", input_params, f"FAILED: {str(e)}")
