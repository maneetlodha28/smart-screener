from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.mapping import Goal, RiskProfile
from app.main import app


def test_interpret_endpoint_maps_fields() -> None:
    client = TestClient(app)
    response = client.post(
        "/interpret",
        json={"text": "I want safe income for 5 years with 10k SIP"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_profile"] == RiskProfile.SAFE.value
    assert data["goal"] == Goal.INCOME.value
    assert data["horizon_years"] == 5
    assert data["budget_inr"] == 10_000


def test_interpret_endpoint_defaults() -> None:
    client = TestClient(app)
    response = client.post("/interpret", json={"text": "Just invest my money"})
    assert response.status_code == 200
    assert response.json() == {
        "risk_profile": RiskProfile.BALANCED.value,
        "goal": Goal.GROWTH.value,
        "horizon_years": 5,
        "budget_inr": 0.0,
    }
