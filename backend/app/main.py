from fastapi import FastAPI
from pydantic import BaseModel
import logging

from app.core.config import get_settings


class HealthResponse(BaseModel):
    status: str


app = FastAPI()
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup() -> None:
    settings = get_settings()
    logger.setLevel(settings.LOG_LEVEL)
    logger.info("APP_ENV=%s LOG_LEVEL=%s", settings.APP_ENV, settings.LOG_LEVEL)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok")
