from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class Ingestor(ABC):
    """Abstract base class for data ingestors."""

    @abstractmethod
    def fetch_metrics(self, symbols: List[str]) -> Dict[str, Dict[str, object]]:
        """Fetch metrics for the provided symbols."""
        raise NotImplementedError
