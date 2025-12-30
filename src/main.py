from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config.settings import settings
from src.models.api import TaskRequest, TaskResponse
from src.nexus.engine import nexus
from src.memory.cortex import cortex
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("AETHER Nexus Starting Up...")
    try:
        await cortex.connect()
    except Exception as e:
        logger.warning(f"Cortex connection failed: {e}")
        
    yield
    # Shutdown
    logger.info("AETHER Nexus Shutting Down...")
    await cortex.disconnect()

app = FastAPI(
    title="AETHER Core API",
    description="Autonomous Executive Task & High-Efficiency Router",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "system": "AETHER Nexus", "env": settings.APP_ENV}

@app.post("/v1/run", response_model=TaskResponse)
async def run_task(request: TaskRequest):
    """
    Execute a task via the Nexus Engine.
    """
    try:
        # Pass intent to Nexus
        response = await nexus.run(request.intent)
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
