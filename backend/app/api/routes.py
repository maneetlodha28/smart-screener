from __future__ import annotations

from typing import Generator


from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter


from app.core.config import get_settings
from app.db.session import get_engine, get_session
from app.services.portfolio import recommend_portfolio
from app.services.nlp.mock_interpreter import MockInterpreter
from app.core.constants import DISCLAIMER


from .schemas import (
    InterpretRequest,
    InterpretResponse,
    RecommendRequest,
    ScreenRequest,
    ScreenResponse,
)

router = APIRouter()

_interpreter = MockInterpreter()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session bound to the configured engine."""
    settings = get_settings()
    engine = get_engine(settings.DATABASE_URL)
    session = get_session(engine)
    try:
        yield session
    finally:
        session.close()


@router.post("/interpret", response_model=InterpretResponse)
@limiter.limit("60/minute")
def interpret_text(payload: InterpretRequest, request: Request) -> InterpretResponse:  # noqa: ARG001
    """Return structured intent parsed from free text."""
    intent = _interpreter.interpret(payload.text)

    return InterpretResponse(**intent)


@router.post("/screen", response_model=ScreenResponse)
def screen_portfolio(
    request: ScreenRequest, db: Session = Depends(get_db)
) -> ScreenResponse:
    """Return a recommended portfolio for the given input parameters."""
    result = recommend_portfolio(
        db,
        budget_inr=request.budget_inr,
        horizon_years=request.horizon_years,
        risk_profile=request.risk_profile,
        goal=request.goal,
    )
    return ScreenResponse(**result)


@router.post("/recommend", response_model=ScreenResponse)
@limiter.limit("60/minute")
def recommend(
    payload: RecommendRequest, request: Request, db: Session = Depends(get_db)
) -> ScreenResponse:  # noqa: ARG001
    """Interpret free text and return a recommended portfolio."""
    intent = _interpreter.interpret(payload.text)
    if payload.budget_inr is not None:
        intent["budget_inr"] = payload.budget_inr
    if payload.horizon_years is not None:
        intent["horizon_years"] = payload.horizon_years
    if payload.risk_profile is not None:
        intent["risk_profile"] = payload.risk_profile
    if payload.goal is not None:
        intent["goal"] = payload.goal


    if (
        intent.get("budget_inr", 0) <= 0
        or intent.get("horizon_years") is None
        or intent.get("risk_profile") is None
        or intent.get("goal") is None
    ):
        raise HTTPException(status_code=400, detail="Incomplete intent")

    result = recommend_portfolio(
        db,
        budget_inr=intent["budget_inr"],
        horizon_years=intent["horizon_years"],
        risk_profile=intent["risk_profile"],
        goal=intent["goal"],
    )
    return ScreenResponse(**result)

@router.get("/info")
def info() -> dict[str, str]:
    """Return basic disclaimer info."""
    return {"disclaimer": DISCLAIMER}
