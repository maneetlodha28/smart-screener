from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.models import IngestionRun, InstrumentType, Metric
from app.db.session import get_engine, get_session
from app.repositories.instruments import InstrumentRepository
from app.repositories.metrics import MetricRepository
from app.services.ingestion.yf_ingestor import YFIngestor


def ingest(session: Session) -> None:
    """Fetch and persist metrics for all instruments."""
    inst_repo = InstrumentRepository(session)
    metric_repo = MetricRepository(session)
    instruments = inst_repo.list_all()
    symbols = [inst.symbol for inst in instruments]
    data = YFIngestor().fetch_metrics(symbols)
    for inst in instruments:
        m = data.get(inst.symbol)
        if m is None:
            continue
        metric_repo.create(
            Metric(
                instrument_id=inst.id,
                as_of_date=m["as_of_date"],
                price=m["price"],
                pe=m.get("pe") if inst.instrument_type is InstrumentType.STOCK else None,
                dividend_yield=m.get("dividend_yield"),
            )
        )
    session.add(IngestionRun())
    session.commit()


def main() -> None:  # pragma: no cover - wrapper for CLI
    settings = get_settings()
    engine = get_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)
    session = get_session(engine)
    try:
        ingest(session)
    finally:
        session.close()


if __name__ == "__main__":  # pragma: no cover
    main()
