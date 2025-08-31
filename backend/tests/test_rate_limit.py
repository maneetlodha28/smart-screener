from fastapi.testclient import TestClient

from app.main import app


def test_rate_limit_on_interpret_and_recommend() -> None:
    client = TestClient(app)

    # Exceed limit on /interpret
    for _ in range(60):
        res = client.post("/interpret", json={"text": "hello"})
        assert res.status_code == 200
    res = client.post("/interpret", json={"text": "hello"})
    assert res.status_code == 429
    assert "retry-after" in {k.lower(): v for k, v in res.headers.items()}

    # Exceed limit on /recommend
    for _ in range(60):
        res = client.post("/recommend", json={"text": "hi"})
        assert res.status_code in (200, 400)
    res = client.post("/recommend", json={"text": "hi"})
    assert res.status_code == 429
    assert "retry-after" in {k.lower(): v for k, v in res.headers.items()}
