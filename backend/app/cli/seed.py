from __future__ import annotations

from typing import Sequence

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.models import Instrument, InstrumentType
from app.db.session import get_engine, get_session
from app.repositories.instruments import InstrumentRepository

# Instruments to seed with minimal realistic metadata
SEED_INSTRUMENTS: Sequence[dict[str, object]] = [
    {
        "symbol": "RELIANCE.NS",
        "name": "Reliance Industries",
        "instrument_type": InstrumentType.STOCK,
        "sector": "Energy",
    },
    {
        "symbol": "HDFCBANK.NS",
        "name": "HDFC Bank",
        "instrument_type": InstrumentType.STOCK,
        "sector": "Financial Services",
    },
    {
        "symbol": "INFY.NS",
        "name": "Infosys",
        "instrument_type": InstrumentType.STOCK,
        "sector": "Information Technology",
    },
    {
        "symbol": "NIFTYBEES.NS",
        "name": "Nippon India ETF Nifty BeES",
        "instrument_type": InstrumentType.ETF,
        "sector": "Index",
    },
]


def seed(session: Session) -> None:
    """Seed the database with a minimal set of instruments.

    Re-running the function is idempotent thanks to upsert semantics.
    """
    repo = InstrumentRepository(session)
    for data in SEED_INSTRUMENTS:
        repo.upsert_by_symbol(Instrument(**data))


def main() -> None:  # pragma: no cover - thin wrapper for CLI use
    settings = get_settings()
    engine = get_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)
    session = get_session(engine)
    try:
        seed(session)
    finally:
        session.close()


if __name__ == "__main__":  # pragma: no cover - module execution
    main()
