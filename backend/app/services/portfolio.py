from __future__ import annotations

from typing import Dict, List

from sqlalchemy.orm import Session

from app.domain.mapping import Goal, RiskProfile, map_intent_to_filters
from app.domain.filtering import filter_candidates
from app.domain.allocation import allocate
from app.domain.explain import explain_instrument, explain_portfolio
from app.core.constants import DISCLAIMER
from app.repositories.metrics import MetricRepository
from app.repositories.instruments import InstrumentRepository


def recommend_portfolio(
    session: Session,
    budget_inr: float,
    horizon_years: int,
    risk_profile: RiskProfile,
    goal: Goal,
) -> dict:
    """Produce a mini-portfolio for the given parameters.

    The function orchestrates mapping of user intent to filter thresholds,
    candidate filtering, budget allocation, and generation of natural
    language explanations.  All database interactions are read-only via the
    supplied ``session``.
    """

    filters = map_intent_to_filters(risk_profile, goal, horizon_years)
    candidates = filter_candidates(session, filters)
    allocations = allocate(candidates, budget_inr, filters)

    inst_repo = InstrumentRepository(session)
    metric_repo = MetricRepository(session)

    instruments_payload: List[Dict] = []
    instrument_explanations: Dict[str, str] = {}

    for alloc in allocations:
        inst = inst_repo.get_by_symbol(alloc.symbol)
        if inst is None:
            continue

        metric = metric_repo.latest_by_instrument(alloc.symbol)

        instruments_payload.append(
            {
                "symbol": inst.symbol,
                "name": inst.name,
                "instrument_type": inst.instrument_type.value,
                "sector": inst.sector,
                "metric": {
                    "as_of_date": metric.as_of_date.isoformat() if metric else None,
                    "price": metric.price if metric else None,
                    "pe": metric.pe if metric else None,
                    "roe": metric.roe if metric else None,
                    "dividend_yield": metric.dividend_yield if metric else None,
                    "debt_to_equity": metric.debt_to_equity if metric else None,
                    "revenue_growth": metric.revenue_growth if metric else None,
                    "earnings_growth": metric.earnings_growth if metric else None,
                },
            }
        )

        instrument_explanations[alloc.symbol] = explain_instrument(
            inst, metric, risk_profile, goal
        )

    portfolio_text = explain_portfolio(
        allocations, risk_profile, goal, horizon_years
    )

    return {
        "allocations": [a.__dict__ for a in allocations],
        "instruments": instruments_payload,
        "explanations": {
            "portfolio": portfolio_text,
            "instruments": instrument_explanations,
        },
        "disclaimer": DISCLAIMER,

    }
