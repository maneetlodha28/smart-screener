from __future__ import annotations

from app.db.models import Instrument, InstrumentType
from app.domain.allocation import allocate
from app.domain.mapping import Goal, RiskProfile, map_intent_to_filters


def _candidates():
    return [
        Instrument(
            symbol="RELIANCE",
            name="Reliance Industries",
            instrument_type=InstrumentType.STOCK,
            sector="Energy",
        ),
        Instrument(
            symbol="HDFCBANK",
            name="HDFC Bank",
            instrument_type=InstrumentType.STOCK,
            sector="Finance",
        ),
        Instrument(
            symbol="INFY",
            name="Infosys",
            instrument_type=InstrumentType.STOCK,
            sector="Technology",
        ),
        Instrument(
            symbol="NIFTYBEES",
            name="Nifty ETF",
            instrument_type=InstrumentType.ETF,
        ),
    ]


def test_safe_profile_allocates_with_etf_and_budget_sum():
    filters = map_intent_to_filters(RiskProfile.SAFE, Goal.INCOME, 5)
    allocations = allocate(_candidates(), 10000, filters)

    assert len(allocations) == filters.max_instruments
    assert sum(a.percent for a in allocations) == 100
    total = sum(a.amount_inr for a in allocations)
    assert abs(total - 10000) <= 1
    symbols = {a.symbol for a in allocations}
    assert "NIFTYBEES" in symbols


def test_aggressive_profile_excludes_etf():
    filters = map_intent_to_filters(RiskProfile.AGGRESSIVE, Goal.GROWTH, 5)
    allocations = allocate(_candidates(), 15000, filters)

    assert 3 <= len(allocations) <= 5
    assert sum(a.percent for a in allocations) == 100
    total = sum(a.amount_inr for a in allocations)
    assert abs(total - 15000) <= 1
    symbols = {a.symbol for a in allocations}
    assert "NIFTYBEES" not in symbols
