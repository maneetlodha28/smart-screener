from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FilterParams:
    """Parameters for filtering instruments.

    All numeric fields are expressed in their natural units.  The mapping
    function is responsible for translating user intent into concrete
    thresholds.
    """

    min_market_cap: float
    max_de_ratio: float
    min_roe: float
    min_div_yield: float
    growth_bias: bool
    max_instruments: int
    include_etfs: bool
