from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.db.models import Instrument, InstrumentType
from .types import FilterParams


@dataclass(frozen=True)
class AllocationItem:
    """Allocation result for a single instrument."""

    symbol: str
    percent: int
    amount_inr: int


def allocate(
    candidates: List[Instrument], budget: float, filters: FilterParams
) -> List[AllocationItem]:
    """Allocate a budget across candidate instruments.

    The allocation is deterministic and aims for slight diversification across
    instrument types and sectors.  ETFs are included if ``filters.include_etfs``
    is true and present in ``candidates``.  Percentages are equal-weighted and
    corrected so that the total sums to exactly 100.
    """

    if not candidates or filters.max_instruments <= 0:
        return []

    selected: list[Instrument] = []

    if filters.include_etfs:
        etfs = [c for c in candidates if c.instrument_type == InstrumentType.ETF]
        if etfs:
            selected.append(etfs[0])

    remaining = [c for c in candidates if c not in selected]
    remaining.sort(key=lambda i: (i.instrument_type.value, i.sector or "", i.symbol))

    seen_sectors = {inst.sector for inst in selected}
    for inst in remaining:
        if len(selected) >= filters.max_instruments:
            break
        if inst.sector not in seen_sectors:
            selected.append(inst)
            seen_sectors.add(inst.sector)

    if len(selected) < min(filters.max_instruments, len(candidates)):
        for inst in remaining:
            if len(selected) >= min(filters.max_instruments, len(candidates)):
                break
            if inst not in selected:
                selected.append(inst)

    selected = selected[: min(filters.max_instruments, len(candidates))]
    n = len(selected)
    if n == 0:
        return []

    base = 100 // n
    percents = [base] * n
    residual = 100 - base * n
    for i in range(residual):
        percents[i] += 1

    amounts = [int(round(budget * p / 100)) for p in percents]
    diff = int(round(budget)) - sum(amounts)
    if diff != 0:
        amounts[0] += diff

    return [
        AllocationItem(symbol=inst.symbol, percent=percent, amount_inr=amt)
        for inst, percent, amt in zip(selected, percents, amounts)
    ]
