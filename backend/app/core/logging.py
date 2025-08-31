import contextvars
import json
import logging
import sys
from typing import Any, Dict

# Context variable storing current request id
request_id_ctx_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)


class JSONFormatter(logging.Formatter):
    """Format log records as JSON with optional request context."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        data: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }
        request_id = getattr(record, "request_id", None) or request_id_ctx_var.get()
        if request_id:
            data["request_id"] = request_id
        # Include common extras when present
        for attr in ("path", "method", "status_code", "app_env", "log_level"):
            if hasattr(record, attr):
                data[attr] = getattr(record, attr)
        return json.dumps(data)


def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logger to emit JSON-formatted logs."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
