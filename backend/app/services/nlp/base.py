from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypedDict

from app.domain.mapping import Goal, RiskProfile


class Intent(TypedDict, total=False):
    """Structured intent extracted from free text."""

    budget_inr: float
    horizon_years: int
    risk_profile: RiskProfile
    goal: Goal


class IntentInterpreter(ABC):
    """Interpret natural language into a structured intent."""

    @abstractmethod
    def interpret(self, text: str) -> Intent:
        """Return fields derived from ``text``.

        Implementations must be deterministic and side-effect free.
        """
        raise NotImplementedError
