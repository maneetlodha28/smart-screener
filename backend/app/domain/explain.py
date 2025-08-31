from __future__ import annotations

from typing import Iterable, List

from app.db.models import Instrument, Metric
from .allocation import AllocationItem
from .mapping import Goal, RiskProfile


def _fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def explain_instrument(
    instrument: Instrument,
    latest_metric: Metric | None,
    risk_profile: RiskProfile,
    goal: Goal,
) -> str:
    parts: List[str] = [f"{instrument.name} ({instrument.symbol})"]

    if latest_metric:
        parts.append(
            f"priced at ₹{latest_metric.price:.2f} as of {latest_metric.as_of_date.isoformat()}"
        )
        if latest_metric.pe is not None:
            parts.append(f"P/E {latest_metric.pe:.1f}")
        if latest_metric.roe is not None:
            parts.append(f"ROE {_fmt_pct(latest_metric.roe)}")
        if latest_metric.dividend_yield is not None:
            parts.append(f"dividend yield {_fmt_pct(latest_metric.dividend_yield)}")
    else:
        parts.append("with no recent metrics available")

    risk_notes = {
        RiskProfile.SAFE: "adds stability",
        RiskProfile.BALANCED: "offers balanced growth",
        RiskProfile.AGGRESSIVE: "pursues higher growth"
    }
    parts.append(risk_notes[risk_profile])
    parts.append(f"for your {goal.value} goal.")
    return " ".join(parts)


def explain_portfolio(
    allocations: Iterable[AllocationItem],
    risk_profile: RiskProfile,
    goal: Goal,
    horizon_years: int,
) -> str:
    count = len(list(allocations))
    risk_guidance = {
        RiskProfile.SAFE: "focuses on capital preservation",
        RiskProfile.BALANCED: "balances stability and growth",
        RiskProfile.AGGRESSIVE: "targets higher returns with higher volatility",
    }
    return (
        f"This {risk_profile.value} portfolio for {goal.value} over {horizon_years} years "
        f"spreads across {count} instruments and {risk_guidance[risk_profile]}."
    )
