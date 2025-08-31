import json
import logging
from fastapi.testclient import TestClient

from app.main import app


def test_metrics_returns_uptime() -> None:
    with TestClient(app) as client:
        response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["uptime_seconds"] > 0


def test_request_logging_includes_request_id(caplog) -> None:
    client = TestClient(app)
    with caplog.at_level(logging.INFO):
        client.get("/health")
    record = next(r for r in caplog.records if r.getMessage() == "request")
    formatter = logging.getLogger().handlers[0].formatter
    line = formatter.format(record)
    parsed = json.loads(line)
    assert "request_id" in parsed
    assert parsed["path"] == "/health"
    assert parsed["method"] == "GET"
    assert parsed["status_code"] == 200
