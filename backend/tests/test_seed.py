from __future__ import annotations

from app.cli.seed import seed
from app.db.base import Base
from app.db.models import Instrument
from app.db.session import get_engine, get_session


def test_seed_inserts_unique_instruments() -> None:
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = get_session(engine)

    try:
        seed(session)
        instruments = session.query(Instrument).all()
        assert len(instruments) == 4
        assert {i.symbol for i in instruments} == {
            "RELIANCE.NS",
            "HDFCBANK.NS",
            "INFY.NS",
            "NIFTYBEES.NS",
        }

        seed(session)
        assert session.query(Instrument).count() == 4
    finally:
        session.close()
