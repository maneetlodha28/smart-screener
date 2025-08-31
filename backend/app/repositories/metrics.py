from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import Instrument, Metric


class MetricRepository:
    """Repository for operations on Metric entities."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, metric: Metric) -> Metric:
        """Insert a new metric record."""
        self._session.add(metric)
        self._session.commit()
        self._session.refresh(metric)
        return metric

    def list_by_instrument(self, symbol: str) -> list[Metric]:
        """List metrics for a given instrument symbol ordered by date."""
        return (
            self._session.query(Metric)
            .join(Instrument)
            .filter(Instrument.symbol == symbol)
            .order_by(Metric.as_of_date)
            .all()
        )

    def latest_by_instrument(self, symbol: str) -> Metric | None:
        """Return the most recent metric for an instrument symbol."""
        return (
            self._session.query(Metric)
            .join(Instrument)
            .filter(Instrument.symbol == symbol)
            .order_by(Metric.as_of_date.desc())
            .first()
        )
