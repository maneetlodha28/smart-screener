from __future__ import annotations

import time
from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.config import get_settings

router = APIRouter()


class MetricsResponse(BaseModel):
    build: str
    uptime_seconds: float


@router.get("/metrics", response_model=MetricsResponse)
def metrics(request: Request) -> MetricsResponse:
    """Return basic build info and process uptime."""
    settings = get_settings()
    uptime = time.time() - request.app.state.start_time
    return MetricsResponse(build=settings.APP_ENV, uptime_seconds=uptime)
