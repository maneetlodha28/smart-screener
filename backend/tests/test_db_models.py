from datetime import date

from app.db.base import Base
from app.db.models import Instrument, InstrumentType, Metric
from app.db.session import get_engine, get_session


def test_insert_instrument_and_metric() -> None:
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = get_session(engine)

    instrument = Instrument(symbol="INFY", name="Infosys", instrument_type=InstrumentType.STOCK)
    session.add(instrument)
    session.commit()
    session.refresh(instrument)

    metric = Metric(
        instrument_id=instrument.id,
        as_of_date=date(2024, 1, 1),
        price=100.0,
    )
    session.add(metric)
    session.commit()

    result = session.query(Metric).filter_by(instrument_id=instrument.id).one()
    assert result.price == 100.0
    assert result.instrument_id == instrument.id
