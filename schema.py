"""
Normalized trade schema — unified representation across Binance and Bybit.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NormalizedTrade:
    """Unified trade record for behavioral analysis."""

    trade_id: str
    timestamp: datetime
    symbol: str
    side: str  # LONG | SHORT (derived from Buy/Sell + position)
    price: float
    qty: float
    pnl: float  # Realized PnL in quote (USDT)
    fee: float
    leverage: float  # 1.0 if unknown
    position_size_pct: Optional[float] = None  # % of account if available
    exchange: str = ""
    raw: Optional[dict] = None
