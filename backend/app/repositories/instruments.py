from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import Instrument


class InstrumentRepository:
    """Repository for CRUD operations on Instrument entities."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, instrument: Instrument) -> Instrument:
        """Insert a new instrument."""
        self._session.add(instrument)
        self._session.commit()
        self._session.refresh(instrument)
        return instrument

    def get_by_symbol(self, symbol: str) -> Instrument | None:
        """Retrieve an instrument by its symbol."""
        return (
            self._session.query(Instrument)
            .filter(Instrument.symbol == symbol)
            .first()
        )

    def list_all(self) -> list[Instrument]:
        """Return all instruments."""
        return self._session.query(Instrument).all()

    def upsert_by_symbol(self, instrument: Instrument) -> Instrument:
        """Create or update an instrument based on its symbol."""
        existing = self.get_by_symbol(instrument.symbol)
        if existing is not None:
            existing.name = instrument.name
            existing.instrument_type = instrument.instrument_type
            existing.sector = instrument.sector
            existing.market_cap = instrument.market_cap
            existing.exchange = instrument.exchange
            self._session.commit()
            self._session.refresh(existing)
            return existing
        return self.create(instrument)
