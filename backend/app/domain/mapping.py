from __future__ import annotations

from enum import Enum

from .types import FilterParams


class RiskProfile(str, Enum):
    """Investor risk appetite."""

    SAFE = "safe"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"


class Goal(str, Enum):
    """High level investment intent."""

    INCOME = "income"
    GROWTH = "growth"


def map_intent_to_filters(
    risk_profile: RiskProfile, goal: Goal, horizon_years: int
) -> FilterParams:
    """Translate user intent into concrete filter parameters.

    The mapping is deterministic and uses simple heuristics derived from
    conventional investing wisdom.  ``horizon_years`` is accepted for future
    refinements but currently does not alter the result.
    """

    if risk_profile is RiskProfile.SAFE:
        return FilterParams(
            min_market_cap=1e11,  # large caps for stability
            max_de_ratio=0.5,  # low leverage preferred
            min_roe=0.0,
            min_div_yield=0.03 if goal is Goal.INCOME else 0.01,
            growth_bias=goal is Goal.GROWTH,
            max_instruments=3,
            include_etfs=True,
        )

    if risk_profile is RiskProfile.BALANCED:
        return FilterParams(
            min_market_cap=5e10,  # mid to large caps
            max_de_ratio=1.0,
            min_roe=0.10,
            min_div_yield=0.02 if goal is Goal.INCOME else 0.005,
            growth_bias=goal is Goal.GROWTH,
            max_instruments=4,
            include_etfs=True,
        )

    # Aggressive profile
    return FilterParams(
        min_market_cap=1e10,  # allow smaller companies
        max_de_ratio=2.0,
        min_roe=0.15,
        min_div_yield=0.0 if goal is Goal.GROWTH else 0.01,
        growth_bias=True,
        max_instruments=5,
        include_etfs=False,
    )
