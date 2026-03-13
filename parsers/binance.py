"""
Binance CSV parser — supports Futures trade/transaction history exports.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from schema import NormalizedTrade


def _col(row: dict, *names: str, default="") -> str:
    for n in names:
        for k, v in row.items():
            if k.strip().lower() == n.lower():
                return (v or "").strip()
    return default


def _num(row: dict, *names: str, default: float = 0.0) -> float:
    s = _col(row, *names)
    if not s:
        return default
    s = s.replace(",", "").replace(" ", "")
    try:
        return float(s)
    except ValueError:
        return default


def _ts(s: str, row: dict) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip()
    # Try Unix ms
    if s.isdigit():
        ms = int(s)
        if ms > 1e12:  # ms
            return datetime.utcfromtimestamp(ms / 1000.0)
        if ms > 1e9:  # seconds
            return datetime.utcfromtimestamp(ms)
    # Try ISO / common formats
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d-%m-%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
    ):
        try:
            return datetime.strptime(s[:19], fmt)
        except (ValueError, TypeError):
            continue
    return None


def _side(raw: str, position_side: str) -> str:
    raw = raw.upper()
    pos = position_side.upper()
    if "LONG" in pos or "BUY" in raw:
        return "LONG"
    if "SHORT" in pos or "SELL" in raw:
        return "SHORT"
    return "LONG" if "BUY" in raw else "SHORT"


def parse_binance_csv(path: Path) -> List[NormalizedTrade]:
    """
    Parse Binance Futures CSV export.
    Handles: Date, Time, time, Pair, Symbol, Side, Type, Order Price, Price,
    Filled, Qty, qty, Realized PnL, realizedPnl, Commission, Fee, Position Side, etc.
    """
    trades: List[NormalizedTrade] = []
    seen: set[str] = set()

    with open(path, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if not row:
                continue
            ts_str = _col(row, "time", "date", "timestamp", "datetime")
            ts = _ts(ts_str, row)
            if not ts:
                continue

            symbol = _col(row, "symbol", "pair", "market") or "UNKNOWN"
            side_raw = _col(row, "side", "type")
            pos_side = _col(row, "position side", "positionside", "position")
            side = _side(side_raw, pos_side)

            price = _num(row, "price", "order price", "execution price", "fill price")
            qty = _num(row, "qty", "filled", "filled quantity", "quantity", "amount")
            pnl = _num(row, "realized pnl", "realizedpnl", "realized p&l", "pnl", "profit")
            fee = _num(row, "commission", "fee", "trading fee", "fees")
            lev = _num(row, "leverage", "lev", "posleverage")

            trade_id = _col(row, "id", "trade id", "tradeid") or f"binance_{i}"

            if trade_id in seen:
                continue
            seen.add(trade_id)

            leverage = lev if lev > 0 else 1.0

            trades.append(
                NormalizedTrade(
                    trade_id=trade_id,
                    timestamp=ts,
                    symbol=symbol,
                    side=side,
                    price=price if price > 0 else 1.0,
                    qty=qty,
                    pnl=pnl,
                    fee=fee,
                    leverage=leverage,
                    exchange="binance",
                    raw=dict(row),
                )
            )

    return trades
