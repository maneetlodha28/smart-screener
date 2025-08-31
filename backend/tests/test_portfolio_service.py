from __future__ import annotations

from datetime import date

from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_engine, get_session
from app.domain.mapping import Goal, RiskProfile
from app.services.portfolio import recommend_portfolio


def _seed_session():
    engine = get_engine("sqlite:///:memory:")
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


def test_recommend_portfolio_balanced_growth():
    session = _seed_session()
    result = recommend_portfolio(
        session,
        budget_inr=10000,
        horizon_years=5,
        risk_profile=RiskProfile.BALANCED,
        goal=Goal.GROWTH,
    )

    allocations = result["allocations"]
    assert len(allocations) == 3
    assert sum(a["percent"] for a in allocations) == 100
    assert abs(sum(a["amount_inr"] for a in allocations) - 10000) <= 1

    symbols = [a["symbol"] for a in allocations]
    assert symbols[0] == "NIFTYBEES"
    assert set(symbols) == {"NIFTYBEES", "RELIANCE", "HDFCBANK"}

    assert len(result["instruments"]) == 3
    for inst in result["instruments"]:
        assert inst["metric"]["price"] is not None

    explanations = result["explanations"]
    assert explanations["portfolio"]
    assert len(explanations["instruments"]) == 3
    assert result["disclaimer"]
