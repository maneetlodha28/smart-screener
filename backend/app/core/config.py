from functools import lru_cache
from typing import Literal, List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str = "sqlite:///:memory:"
    AI_PROVIDER: Literal["mock", "openai"] = "mock"
    AI_API_KEY: str | None = None
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
