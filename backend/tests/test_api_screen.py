from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_session
from app.domain.mapping import Goal, RiskProfile
from app.main import app
from app.api import routes


def _seed_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    session = get_session(engine)

    instruments = [
        Instrument(
            symbol="RELIANCE",
            name="Reliance Industries",
            instrument_type=InstrumentType.STOCK,
            sector="Energy",
            market_cap=1.5e12,
        ),
        Instrument(
            symbol="HDFCBANK",
            name="HDFC Bank",
            instrument_type=InstrumentType.STOCK,
            sector="Finance",
            market_cap=8e10,
        ),
        Instrument(
            symbol="NIFTYBEES",
            name="Nifty ETF",
            instrument_type=InstrumentType.ETF,
        ),
    ]
    session.add_all(instruments)
    session.flush()

    session.add(
        Metric(
            instrument_id=instruments[0].id,
            as_of_date=date(2023, 1, 1),
            price=100.0,
            roe=0.12,
            debt_to_equity=0.3,
            dividend_yield=0.04,
            revenue_growth=0.05,
            earnings_growth=0.06,
        )
    )
    session.add(
        Metric(
            instrument_id=instruments[1].id,
            as_of_date=date(2023, 1, 1),
            price=100.0,
            roe=0.14,
            debt_to_equity=0.9,
            dividend_yield=0.01,
            revenue_growth=0.04,
            earnings_growth=0.05,
        )
    )
    session.add(
        Metric(
            instrument_id=instruments[2].id,
            as_of_date=date(2023, 1, 1),
            price=50.0,
        )
    )

    session.commit()
    return session


def test_screen_endpoint_returns_portfolio():
    session = _seed_session()
    app.dependency_overrides[routes.get_db] = lambda: session

    client = TestClient(app)
    response = client.post(
        "/screen",
        json={
            "budget_inr": 10000,
            "horizon_years": 5,
            "risk_profile": RiskProfile.BALANCED.value,
            "goal": Goal.GROWTH.value,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["allocations"]) == 3
    assert sum(a["percent"] for a in data["allocations"]) == 100
    assert "portfolio" in data["explanations"]
    assert data["disclaimer"]

    app.dependency_overrides.clear()


def test_screen_endpoint_validation():
    client = TestClient(app)
    response = client.post(
        "/screen",
        json={
            "budget_inr": -1,
            "horizon_years": 5,
            "risk_profile": RiskProfile.BALANCED.value,
            "goal": Goal.GROWTH.value,
        },
    )
    assert response.status_code == 422
