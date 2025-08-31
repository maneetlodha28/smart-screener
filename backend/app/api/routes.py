from __future__ import annotations

from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_engine, get_session
from app.services.portfolio import recommend_portfolio
from app.services.nlp.mock_interpreter import MockInterpreter

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
def interpret_text(request: InterpretRequest) -> InterpretResponse:
    """Return structured intent parsed from free text."""
    intent = _interpreter.interpret(request.text)
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
def recommend(
    request: RecommendRequest, db: Session = Depends(get_db)
) -> ScreenResponse:
    """Interpret free text and return a recommended portfolio."""
    intent = _interpreter.interpret(request.text)
    if request.budget_inr is not None:
        intent["budget_inr"] = request.budget_inr
    if request.horizon_years is not None:
        intent["horizon_years"] = request.horizon_years
    if request.risk_profile is not None:
        intent["risk_profile"] = request.risk_profile
    if request.goal is not None:
        intent["goal"] = request.goal

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
