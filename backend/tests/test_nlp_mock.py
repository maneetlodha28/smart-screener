from __future__ import annotations

from app.domain.mapping import Goal, RiskProfile
from app.services.nlp.mock_interpreter import MockInterpreter


def test_interpret_full_prompt() -> None:
    interp = MockInterpreter()
    res = interp.interpret("I want safe income for 5 years with 10k SIP")
    assert res["risk_profile"] == RiskProfile.SAFE
    assert res["goal"] == Goal.INCOME
    assert res["horizon_years"] == 5
    assert res["budget_inr"] == 10_000


def test_interpret_aggressive_lakh() -> None:
    interp = MockInterpreter()
    res = interp.interpret("Aggressive growth in 3 years, invest 2 lakh")
    assert res["risk_profile"] == RiskProfile.AGGRESSIVE
    assert res["goal"] == Goal.GROWTH
    assert res["horizon_years"] == 3
    assert res["budget_inr"] == 200_000


def test_interpret_defaults() -> None:
    interp = MockInterpreter()
    res = interp.interpret("Just invest my money")
    assert res == {
        "risk_profile": RiskProfile.BALANCED,
        "goal": Goal.GROWTH,
        "horizon_years": 5,
        "budget_inr": 0.0,
    }
