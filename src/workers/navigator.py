import logging
from playwright.async_api import async_playwright
from src.workers.base import BaseAgent
from src.models.artifacts import ActionArtifact

logger = logging.getLogger(__name__)

class Navigator(BaseAgent):
    """
    The Navigator: Responsible for Web Browsing and Search.
    """
    def __init__(self):
        super().__init__(agent_id="NAVIGATOR_001")

    async def execute(self, step_data: dict) -> ActionArtifact:
        """
        Executes web-related tasks.
        """
        action = step_data.get("action", "").upper()
        url = step_data.get("url")
        query = step_data.get("query")
        
        input_params = {"action": action, "url": url, "query": query}
        
        try:
            if action == "FETCH":
                if not url:
                    return self._create_artifact("FETCH_URL", input_params, "FAILED: Missing URL")
                return await self._fetch_url(url, input_params)
            elif action == "SEARCH":
                if not query:
                    return self._create_artifact("WEB_SEARCH", input_params, "FAILED: Missing query")
                return await self._search_web(query, input_params)
            else:
                return self._create_artifact("UNKNOWN", input_params, f"FAILED: Unsupported action: {action}")
        except Exception as e:
            logger.error(f"Error in Navigator execution: {e}")
            return self._create_artifact(action, input_params, f"FAILED: {str(e)}")

    async def _fetch_url(self, url: str, input_params: dict) -> ActionArtifact:
        async with async_playwright() as p:
            # Note: Launching browser every time is inefficient, but safe for now.
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url, timeout=30000)
                title = await page.title()
                result = f"SUCCESS: Fetched '{title}'. Content length: {len(await page.content())}"
            except Exception as e:
                result = f"FAILED: {str(e)}"
            finally:
                await browser.close()
                
        return self._create_artifact("FETCH_URL", input_params, result)

    async def _search_web(self, query: str, input_params: dict) -> ActionArtifact:
        # Mock Search
        logger.info(f"Mocking search for: {query}")
        result = f"SUCCESS: Found 2 results for '{query}' (Mock Data)"
        return self._create_artifact("WEB_SEARCH", input_params, result)
