from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, conint, confloat

from app.domain.mapping import Goal, RiskProfile


class ScreenRequest(BaseModel):
    """Request model for the /screen endpoint."""

    budget_inr: confloat(gt=0) = Field(
        ..., description="Total investment budget in INR"
    )
    horizon_years: conint(ge=1) = Field(..., description="Investment horizon in years")
    risk_profile: RiskProfile
    goal: Goal


class Allocation(BaseModel):
    symbol: str
    percent: float
    amount_inr: float


class MetricPayload(BaseModel):
    as_of_date: Optional[str]
    price: Optional[float]
    pe: Optional[float]
    roe: Optional[float]
    dividend_yield: Optional[float]
    debt_to_equity: Optional[float]
    revenue_growth: Optional[float]
    earnings_growth: Optional[float]


class InstrumentPayload(BaseModel):
    symbol: str
    name: str
    instrument_type: str
    sector: Optional[str]
    metric: MetricPayload


class ExplanationsPayload(BaseModel):
    portfolio: str
    instruments: Dict[str, str]


class ScreenResponse(BaseModel):
    allocations: List[Allocation]
    instruments: List[InstrumentPayload]
    explanations: ExplanationsPayload


class InterpretRequest(BaseModel):
    """Request payload for the /interpret endpoint."""

    text: str


class InterpretResponse(BaseModel):
    """Structured intent extracted from free text."""

    budget_inr: Optional[float] = None
    horizon_years: Optional[int] = None
    risk_profile: Optional[RiskProfile] = None
    goal: Optional[Goal] = None


class RecommendRequest(InterpretRequest):
    """Request payload for the /recommend endpoint."""

    budget_inr: Optional[confloat(gt=0)] = Field(
        None, description="Override budget in INR if provided"
    )
    horizon_years: Optional[conint(ge=1)] = Field(
        None, description="Override investment horizon"
    )
    risk_profile: Optional[RiskProfile] = None
    goal: Optional[Goal] = None
