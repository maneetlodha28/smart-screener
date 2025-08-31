from __future__ import annotations

from datetime import date

from app.db.models import Instrument, InstrumentType, Metric
from app.domain.allocation import AllocationItem
from app.domain.explain import explain_instrument, explain_portfolio
from app.domain.mapping import Goal, RiskProfile


def _instrument_and_metric():
    instrument = Instrument(
        symbol="INFY",
        name="Infosys",
        instrument_type=InstrumentType.STOCK,
        sector="Tech",
    )
    metric = Metric(
        instrument_id=1,
        as_of_date=date(2024, 1, 1),
        price=1500.0,
        pe=15.0,
        roe=0.20,
        dividend_yield=0.015,
    )
    return instrument, metric


def test_explain_instrument_with_metrics():
    inst, metric = _instrument_and_metric()
    text = explain_instrument(inst, metric, RiskProfile.BALANCED, Goal.GROWTH)
    assert "P/E 15.0" in text
    assert "ROE 20.0%" in text
    assert "dividend yield 1.5%" in text


def test_explain_instrument_missing_metrics():
    inst, _ = _instrument_and_metric()
    text = explain_instrument(inst, None, RiskProfile.SAFE, Goal.INCOME)
    assert "no recent metrics" in text.lower()
    assert "P/E" not in text


def test_explain_portfolio_risk_guidance_changes():
    allocations = [AllocationItem(symbol="INFY", percent=50, amount_inr=5000)]
    safe = explain_portfolio(allocations, RiskProfile.SAFE, Goal.INCOME, 5)
    aggressive = explain_portfolio(allocations, RiskProfile.AGGRESSIVE, Goal.GROWTH, 5)
    assert "capital preservation" in safe
    assert "higher returns" in aggressive
