from __future__ import annotations

from typing import Dict, List, Optional

import yfinance as yf

from .base import Ingestor


class YFIngestor(Ingestor):
    """yfinance-backed ingestor for EOD price and basic metrics."""

    def fetch_metrics(self, symbols: List[str]) -> Dict[str, Dict[str, object]]:
        results: Dict[str, Dict[str, object]] = {}
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if hist.empty:
                continue
            price = float(hist["Close"].iloc[-1])
            as_of_date = hist.index[-1].date()
            info: Dict[str, Optional[float]] = getattr(ticker, "info", {}) or {}
            pe = info.get("trailingPE")
            div_yield = info.get("dividendYield")
            results[symbol] = {
                "as_of_date": as_of_date,
                "price": price,
                "pe": float(pe) if pe is not None else None,
                "dividend_yield": float(div_yield) if div_yield is not None else None,
            }
        return results
