"""
Bybit CSV parser — supports Contract Trade History exports.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List

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


def parse_bybit_csv(path: Path) -> List[NormalizedTrade]:
    """
    Parse Bybit Contract Trade History CSV.
    Columns: OrderID, TradeID, Symbol, Side, ExecPrice, ExecQty, ExecValue,
    TradingFee, TradeTime, ClosedSize, etc.
    """
    trades: List[NormalizedTrade] = []
    # Bybit may have multiple rows per closed position; aggregate by TradeID for simplicity
    seen: set[str] = set()

    with open(path, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if not row:
                continue

            ts_str = _col(row, "tradetime", "trade time", "time", "date")
            if not ts_str:
                continue
            ts_str = ts_str.strip()
            if ts_str.isdigit():
                ms = int(ts_str)
                ts = datetime.utcfromtimestamp(ms / 1000.0) if ms > 1e12 else datetime.utcfromtimestamp(ms)
            else:
                try:
                    ts = datetime.strptime(ts_str[:19], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

            symbol = _col(row, "symbol") or "UNKNOWN"
            side_raw = _col(row, "side").upper()
            side = "LONG" if side_raw in ("BUY", "LONG") else "SHORT"

            price = _num(row, "execprice", "exec price", "price")
            qty = _num(row, "execqty", "exec qty", "closedsize", "quantity")
            exec_val = _num(row, "execvalue", "exec value")
            fee = _num(row, "tradingfee", "trading fee", "fee")

            # Bybit "Closed PnL" or "Realized PnL" - varies by export
            pnl = _num(row, "closed pnl", "realized pnl", "pnl", "profit", "realizedpnl")
            if pnl == 0 and exec_val != 0:
                # Some exports don't have PnL; use 0 and rely on classifier context
                pass

            # Leverage: may be in "Leverage" or "Size" context
            lev = _num(row, "leverage", "lev")
            leverage = lev if lev > 0 else 1.0

            trade_id = _col(row, "tradeid", "trade id", "orderid") or f"bybit_{i}"
            if trade_id in seen:
                continue
            seen.add(trade_id)

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
                    exchange="bybit",
                    raw=dict(row),
                )
            )

    return trades
