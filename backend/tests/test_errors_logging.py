import json
import logging
from fastapi.testclient import TestClient

from app.main import app


@app.get("/boom")
def boom() -> None:  # pragma: no cover - test only
    raise RuntimeError("boom")


def test_error_envelope_contains_request_id(caplog) -> None:
    client = TestClient(app, raise_server_exceptions=False)
    with caplog.at_level(logging.ERROR):
        response = client.get("/boom")
    assert response.status_code == 500
    body = response.json()
    request_id = body["error"]["request_id"]
    record = caplog.records[-1]
    formatter = logging.getLogger().handlers[0].formatter
    log_line = formatter.format(record)
    parsed = json.loads(log_line)
    assert parsed["request_id"] == request_id
    assert parsed["path"] == "/boom"


def test_startup_logs_are_json(caplog) -> None:
    with caplog.at_level(logging.INFO):
        with TestClient(app):
            pass
    record = caplog.records[0]
    formatter = logging.getLogger().handlers[0].formatter
    line = formatter.format(record)
    parsed = json.loads(line)
    assert parsed["message"] == "startup"
    assert "app_env" in parsed
