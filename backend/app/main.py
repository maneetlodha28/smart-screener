import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, request_id_ctx_var


class HealthResponse(BaseModel):
    status: str


configure_logging()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    token = request_id_ctx_var.set(request_id)
    request.state.request_id = request_id
    request.state._request_id_token = token
    response = await call_next(request)
    request_id_ctx_var.reset(token)
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger = logging.getLogger("app")
    logger.exception(
        "Unhandled error",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": 500,
            "request_id": request.state.request_id,
        },
    )
    token = getattr(request.state, "_request_id_token", None)
    if token is not None:
        request_id_ctx_var.reset(token)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "Internal Server Error",
                "request_id": request.state.request_id,
            }
        },
    )


@app.on_event("startup")
async def startup() -> None:
    settings = get_settings()
    logger = logging.getLogger("app")
    logger.setLevel(settings.LOG_LEVEL)
    logger.info(
        "startup",
        extra={"app_env": settings.APP_ENV, "log_level": settings.LOG_LEVEL},
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="ok")
