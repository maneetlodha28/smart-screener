from __future__ import annotations

from datetime import date

from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_engine, get_session
from app.domain.filtering import filter_candidates
from app.domain.mapping import Goal, RiskProfile, map_intent_to_filters


def _setup_db():
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = get_session(engine)

    instruments = [
        Instrument(
            symbol="RELIANCE",
            name="Reliance Industries",
            instrument_type=InstrumentType.STOCK,
            market_cap=1.5e12,
            exchange="NSE",
        ),
        Instrument(
            symbol="HDFCBANK",
            name="HDFC Bank",
            instrument_type=InstrumentType.STOCK,
            market_cap=8e10,
            exchange="NSE",
        ),
        Instrument(
            symbol="TINY",
            name="Tiny Growth",
            instrument_type=InstrumentType.STOCK,
            market_cap=2e10,
            exchange="NSE",
        ),
        Instrument(
            symbol="NIFTYBEES",
            name="Nifty ETF",
            instrument_type=InstrumentType.ETF,
            exchange="NSE",
        ),
    ]
    session.add_all(instruments)
    session.flush()

    # Metrics for RELIANCE
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

    # Metrics for HDFCBANK
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

    # Two metrics for TINY to ensure latest is used
    session.add(
        Metric(
            instrument_id=instruments[2].id,
            as_of_date=date(2023, 1, 1),
            price=10.0,
            roe=0.05,
            debt_to_equity=1.5,
            revenue_growth=-0.02,
            earnings_growth=-0.01,
        )
    )
    session.add(
        Metric(
            instrument_id=instruments[2].id,
            as_of_date=date(2023, 1, 2),
            price=12.0,
            roe=0.20,
            debt_to_equity=1.5,
            revenue_growth=0.15,
            earnings_growth=0.20,
        )
    )

    # Metrics for ETF
    session.add(
        Metric(
            instrument_id=instruments[3].id,
            as_of_date=date(2023, 1, 1),
            price=50.0,
        )
    )

    session.commit()
    return session



def test_safe_profile_includes_etf_and_large_caps():
    session = _setup_db()
    filters = map_intent_to_filters(RiskProfile.SAFE, Goal.INCOME, 5)
    result = filter_candidates(session, filters)
    symbols = {inst.symbol for inst in result}
    # ETF always included
    assert "NIFTYBEES" in symbols
    # Only RELIANCE meets strict income requirements
    assert "RELIANCE" in symbols
    assert "HDFCBANK" not in symbols
    assert "TINY" not in symbols


def test_balanced_growth_includes_mid_caps_and_etf():
    session = _setup_db()
    filters = map_intent_to_filters(RiskProfile.BALANCED, Goal.GROWTH, 7)
    result = filter_candidates(session, filters)
    symbols = {inst.symbol for inst in result}
    assert symbols == {"NIFTYBEES", "RELIANCE", "HDFCBANK"}


def test_aggressive_growth_focuses_on_high_growth_stocks():
    session = _setup_db()
    filters = map_intent_to_filters(RiskProfile.AGGRESSIVE, Goal.GROWTH, 10)
    result = filter_candidates(session, filters)
    symbols = {inst.symbol for inst in result}
    # ETF excluded and only TINY passes aggressive thresholds using latest metric
    assert symbols == {"TINY"}
