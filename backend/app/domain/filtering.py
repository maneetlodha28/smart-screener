from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.db.models import Instrument, InstrumentType, Metric
from .types import FilterParams


def filter_candidates(session: Session, filters: FilterParams) -> List[Instrument]:
    """Return instruments meeting the given filter criteria.

    The function fetches the latest ``Metric`` for each instrument and applies
    simple threshold based filtering.  ETFs are always included when
    ``filters.include_etfs`` is ``True`` regardless of metric availability.
    The returned list is capped to ``filters.max_instruments * 2`` to leave room
    for later allocation steps.
    """

    candidates: list[Instrument] = []

    # Handle ETFs first if they should be included regardless of metrics.
    if filters.include_etfs:
        etfs = (
            session.query(Instrument)
            .filter(Instrument.instrument_type == InstrumentType.ETF)
            .all()
        )
        candidates.extend(etfs)

    # Consider stock instruments applying metric thresholds.
    stocks = (
        session.query(Instrument)
        .filter(Instrument.instrument_type == InstrumentType.STOCK)
        .all()
    )

    for inst in stocks:
        if inst.market_cap is None or inst.market_cap < filters.min_market_cap:
            continue

        metric = (
            session.query(Metric)
            .filter(Metric.instrument_id == inst.id)
            .order_by(Metric.as_of_date.desc())
            .first()
        )
        if metric is None:
            continue

        if metric.debt_to_equity is None or metric.debt_to_equity > filters.max_de_ratio:
            continue
        if metric.roe is None or metric.roe < filters.min_roe:
            continue
        div_yield = metric.dividend_yield or 0.0
        if div_yield < filters.min_div_yield:
            continue
        if filters.growth_bias:
            if (
                metric.revenue_growth is None
                or metric.earnings_growth is None
                or metric.revenue_growth <= 0
                or metric.earnings_growth <= 0
            ):
                continue

        candidates.append(inst)

    # Order by market cap descending for determinism (ETFs keep insertion order).
    stocks_sorted = sorted(
        [c for c in candidates if c.instrument_type == InstrumentType.STOCK],
        key=lambda i: i.market_cap or 0,
        reverse=True,
    )
    etfs_sorted = [c for c in candidates if c.instrument_type == InstrumentType.ETF]
    ordered = etfs_sorted + stocks_sorted

    return ordered[: filters.max_instruments * 2]
