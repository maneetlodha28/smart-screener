from __future__ import annotations

from datetime import date

from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_engine, get_session
from app.repositories.instruments import InstrumentRepository
from app.repositories.metrics import MetricRepository


def test_repositories_work() -> None:
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = get_session(engine)

    instrument_repo = InstrumentRepository(session)
    metric_repo = MetricRepository(session)

    inst = Instrument(
        symbol="TCS",
        name="Tata Consultancy",
        instrument_type=InstrumentType.STOCK,
        exchange="NSE",
    )
    created = instrument_repo.create(inst)

    # upsert by symbol updates existing record
    instrument_repo.upsert_by_symbol(
        Instrument(
            symbol="TCS",
            name="TCS Ltd",
            instrument_type=InstrumentType.STOCK,
            exchange="NSE",
        )
    )
    fetched = instrument_repo.get_by_symbol("TCS")
    assert fetched is not None
    assert fetched.name == "TCS Ltd"
    assert len(instrument_repo.list_all()) == 1

    metric_repo.create(
        Metric(
            instrument_id=created.id,
            as_of_date=date(2023, 1, 1),
            price=100.0,
        )
    )
    metric_repo.create(
        Metric(
            instrument_id=created.id,
            as_of_date=date(2023, 1, 2),
            price=110.0,
        )
    )

    metrics = metric_repo.list_by_instrument("TCS")
    assert len(metrics) == 2
    latest = metric_repo.latest_by_instrument("TCS")
    assert latest is not None
    assert latest.price == 110.0
