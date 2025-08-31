from __future__ import annotations

from app.domain.mapping import Goal, RiskProfile, map_intent_to_filters


def test_safe_income_filters():
    filters = map_intent_to_filters(RiskProfile.SAFE, Goal.INCOME, horizon_years=5)
    # Emphasize stability and dividends for income seekers.
    assert filters.min_market_cap == 1e11  # large caps only
    assert filters.max_de_ratio == 0.5  # conservative leverage
    assert filters.min_roe == 0.0  # ROE not critical for safety
    assert filters.min_div_yield == 0.03  # strong dividend requirement
    assert not filters.growth_bias  # income focus over growth
    assert filters.max_instruments == 3  # concise allocation
    assert filters.include_etfs  # ETFs allowed for diversification


def test_balanced_growth_filters():
    filters = map_intent_to_filters(RiskProfile.BALANCED, Goal.GROWTH, horizon_years=7)
    # Balanced growth seeks moderate quality with some growth tilt.
    assert filters.min_market_cap == 5e10  # mid/large caps
    assert filters.max_de_ratio == 1.0
    assert filters.min_roe == 0.10  # decent profitability
    assert filters.min_div_yield == 0.005  # dividends optional
    assert filters.growth_bias  # growth orientation
    assert filters.max_instruments == 4  # moderate diversification
    assert filters.include_etfs  # ETFs still acceptable


def test_aggressive_growth_filters():
    filters = map_intent_to_filters(
        RiskProfile.AGGRESSIVE, Goal.GROWTH, horizon_years=10
    )
    # Aggressive growth allows smaller caps and focuses on ROE without dividends.
    assert filters.min_market_cap == 1e10  # smaller companies permitted
    assert filters.max_de_ratio == 2.0  # higher leverage tolerated
    assert filters.min_roe == 0.15  # strong profitability required
    assert filters.min_div_yield == 0.0  # dividends not expected
    assert filters.growth_bias
    assert filters.max_instruments == 5  # broader spread to capture upside
    assert not filters.include_etfs  # direct equities only
