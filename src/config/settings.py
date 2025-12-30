from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Application Settings configuration.
    Loads values from environment variables and .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    GOOGLE_API_KEY: Optional[str] = Field(None, description="API Key for Google Gemini")
    REDIS_URL: str = Field("redis://localhost:6379/0", description="URL for Redis Cortex")
    APP_ENV: str = Field("development", description="Application environment (development/production)")
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    SAFETY_MODE: bool = Field(True, description="Enable safety guardrails for Architect worker")

settings = Settings()
