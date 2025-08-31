from __future__ import annotations

import re

from app.domain.mapping import Goal, RiskProfile

from .base import Intent, IntentInterpreter


class MockInterpreter(IntentInterpreter):
    """Deterministic rule-based intent interpreter used for tests."""

    def interpret(self, text: str) -> Intent:
        lowered = text.lower()
        intent: Intent = {
            "budget_inr": 0.0,
            "horizon_years": 5,
            "risk_profile": RiskProfile.BALANCED,
            "goal": Goal.GROWTH,
        }

        if "safe" in lowered or "conservative" in lowered:
            intent["risk_profile"] = RiskProfile.SAFE
        elif "aggressive" in lowered or "high risk" in lowered:
            intent["risk_profile"] = RiskProfile.AGGRESSIVE
        elif "balanced" in lowered or "moderate" in lowered:
            intent["risk_profile"] = RiskProfile.BALANCED

        if "income" in lowered or "dividend" in lowered:
            intent["goal"] = Goal.INCOME
        elif "growth" in lowered:
            intent["goal"] = Goal.GROWTH

        horizon_match = re.search(r"(\d+)\s*(?:years|year|yrs|yr)", lowered)
        if horizon_match:
            intent["horizon_years"] = int(horizon_match.group(1))

        budget_match = re.search(
            r"(?:invest|with|budget)\s*(\d+(?:\.\d+)?)\s*(k|lakh|lac|crore|cr)?",
            lowered,
        )
        if budget_match:
            num = float(budget_match.group(1))
            unit = budget_match.group(2)
            multiplier = 1.0
            if unit == "k":
                multiplier = 1_000
            elif unit in {"lakh", "lac"}:
                multiplier = 100_000
            elif unit in {"crore", "cr"}:
                multiplier = 10_000_000
            intent["budget_inr"] = num * multiplier

        return intent
