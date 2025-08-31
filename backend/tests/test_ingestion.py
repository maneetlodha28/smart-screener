from __future__ import annotations

import pathlib

import pytest
import vcr

from app.cli.seed import SEED_INSTRUMENTS
from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_engine, get_session
from app.repositories.instruments import InstrumentRepository
from app.repositories.metrics import MetricRepository
from app.services.ingestion.yf_ingestor import YFIngestor


CASSETTE_DIR = pathlib.Path(__file__).parent / "cassettes"


@pytest.mark.parametrize(
    ("inst_index", "cassette_name"),
    [
        (0, "yf_reliance.yaml"),
        (3, "yf_niftybees.yaml"),
    ],
)
def test_ingestion_persists_latest_metrics(inst_index: int, cassette_name: str) -> None:
    engine = get_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = get_session(engine)
    repo = InstrumentRepository(session)
    inst_data = SEED_INSTRUMENTS[inst_index]
    instrument = repo.create(Instrument(**inst_data))
    cassette = CASSETTE_DIR / cassette_name
    with vcr.use_cassette(str(cassette)):
        data = YFIngestor().fetch_metrics([instrument.symbol])
    metrics = data[instrument.symbol]
    metric_repo = MetricRepository(session)
    metric_repo.create(
        Metric(
            instrument_id=instrument.id,
            as_of_date=metrics["as_of_date"],
            price=metrics["price"],
            pe=metrics.get("pe") if instrument.instrument_type is InstrumentType.STOCK else None,
            dividend_yield=metrics.get("dividend_yield"),
        )
    )
    latest = metric_repo.latest_by_instrument(instrument.symbol)
    assert latest is not None
    assert latest.price == metrics["price"]
    if instrument.instrument_type is InstrumentType.ETF:
        assert latest.pe is None
    else:
        assert latest.pe == metrics["pe"]
