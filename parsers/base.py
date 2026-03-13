"""
Base parser utilities and auto-detection.
"""

import csv
from pathlib import Path
from typing import List

from schema import NormalizedTrade

from .binance import parse_binance_csv
from .bybit import parse_bybit_csv


def _peek_headers(path: Path) -> List[str]:
    with open(path, encoding="utf-8", errors="replace") as f:
        row = next(csv.reader(f))
        return [c.strip().lower() for c in row] if row else []


def load_and_detect(csv_path: str | Path, exchange: str | None = None) -> List[NormalizedTrade]:
    """
    Load CSV and parse with appropriate parser.
    If exchange is None, auto-detect from headers.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    headers = _peek_headers(path)
    if not headers:
        raise ValueError("CSV has no headers")

    if exchange:
        ex = exchange.lower()
        if ex == "binance":
            return parse_binance_csv(path)
        if ex == "bybit":
            return parse_bybit_csv(path)
        raise ValueError(f"Unknown exchange: {exchange}")

    # Auto-detect: Bybit has TradeTime, ExecPrice, ExecQty; Binance has various
    if "tradetime" in headers or "execprice" in headers or "execqty" in headers:
        return parse_bybit_csv(path)
    if "time" in headers or "date" in headers or "pair" in headers or "symbol" in headers:
        return parse_binance_csv(path)
    raise ValueError("Could not detect exchange. Use --exchange binance or --exchange bybit")
