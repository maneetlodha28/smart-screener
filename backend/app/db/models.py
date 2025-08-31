from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Date, Enum as SqlEnum, Float, ForeignKey, Integer, String
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class InstrumentType(str, Enum):
    STOCK = "stock"
    ETF = "etf"


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    instrument_type: Mapped[InstrumentType] = mapped_column(
        SqlEnum(InstrumentType), nullable=False
    )
    sector: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    market_cap: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    exchange: Mapped[str] = mapped_column(String, nullable=False, default="NSE")

    metrics: Mapped[list["Metric"]] = relationship(back_populates="instrument")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), nullable=False)
    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    pe: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    roe: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    debt_to_equity: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dividend_yield: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    revenue_growth: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    earnings_growth: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    instrument: Mapped[Instrument] = relationship(back_populates="metrics")
