"""
Behavioral classifier — detects 4 error classes from trade sequence.
REVENGE_TRADING, OVERLEVERAGE, FOMO_ENTRY, LOSS_AVERAGING_DOWN
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

from schema import NormalizedTrade


@dataclass
class FlaggedTrade:
    trade_index: int
    trade: NormalizedTrade
    error_class: str
    severity: str  # CRITICAL | HIGH | MEDIUM | LOW
    reason: str
    pnl_attributed: float


def _median_leverage(trades: List[NormalizedTrade], lookback: int = 14) -> float:
    levs = [t.leverage for t in trades[-lookback:] if t.leverage > 0]
    if not levs:
        return 1.0
    sorted_levs = sorted(levs)
    n = len(sorted_levs)
    return (sorted_levs[n // 2] + sorted_levs[(n - 1) // 2]) / 2


def _get_prev_loss_trades(
    trades: List[NormalizedTrade],
    idx: int,
    window_minutes: int = 10,
) -> List[NormalizedTrade]:
    """Trades that closed at a loss within window before current trade."""
    curr = trades[idx].timestamp
    cutoff = curr - timedelta(minutes=window_minutes)
    out = []
    for i in range(idx - 1, -1, -1):
        t = trades[i]
        if t.timestamp < cutoff:
            break
        if t.pnl < 0:
            out.append(t)
    return out


def classify_trades(
    trades: List[NormalizedTrade],
    config: Optional[dict] = None,
) -> List[FlaggedTrade]:
    """
    Classify trades against 4 error types using rule-based + heuristics.
    """
    config = config or {}
    window_min = config.get("revenge_trading_window_minutes", 10)
    lev_mult = config.get("overleverage_median_multiplier", 2.0)
    fomo_pct = config.get("fomo_candle_threshold_pct", 4.0)

    flagged: List[FlaggedTrade] = []
    for i, t in enumerate(trades):
        # REVENGE_TRADING: entry < 10 min after loss + position size increase >= 1.5x
        prev_losses = _get_prev_loss_trades(trades, i, window_min)
        if prev_losses:
            # Compare to most recent loss trade
            prev_qty = prev_losses[0].qty
            if prev_qty > 0 and t.qty >= prev_qty * 1.5:
                reason = f"Entry placed {window_min} min after prior loss. Position size increased vs prior trade."
                flagged.append(
                    FlaggedTrade(
                        trade_index=i + 1,
                        trade=t,
                        error_class="REVENGE_TRADING",
                        severity="CRITICAL" if t.qty >= prev_qty * 3 else "HIGH",
                        reason=reason,
                        pnl_attributed=t.pnl if t.pnl < 0 else 0,
                    )
                )
                continue

        # OVERLEVERAGE: leverage > 2x personal 14-day median AND large position
        # Need at least 3 prior trades to establish median
        if i >= 3:
            median_lev = _median_leverage(trades[:i], lookback=min(14, i))
            if median_lev > 0 and t.leverage >= median_lev * lev_mult and t.leverage >= 10:
                reason = f"{t.leverage:.0f}x leverage exceeded your median ({median_lev:.0f}x) by {100 * (t.leverage / median_lev - 1):.0f}%."
                flagged.append(
                    FlaggedTrade(
                        trade_index=i + 1,
                        trade=t,
                        error_class="OVERLEVERAGE",
                        severity="HIGH" if t.leverage >= 20 else "MEDIUM",
                        reason=reason,
                        pnl_attributed=t.pnl if t.pnl < 0 else 0,
                    )
                )
                continue

        # FOMO_ENTRY: heuristic — entry after large move (we don't have candle data)
        # Approximate: high leverage + immediate loss = possible FOMO
        if t.leverage >= 10 and t.pnl < -t.qty * t.price * 0.02:  # lost >2% of notional quickly
            reason = "High leverage entry with immediate loss. Possible FOMO at extension."
            flagged.append(
                FlaggedTrade(
                    trade_index=i + 1,
                    trade=t,
                    error_class="FOMO_ENTRY",
                    severity="MEDIUM",
                    reason=reason,
                    pnl_attributed=t.pnl,
                )
            )
            continue

        # LOSS_AVERAGING_DOWN: same-direction add after position goes negative
        # Heuristic: multiple trades same symbol/side in short window, prior was loss
        for j in range(max(0, i - 3), i):
            pt = trades[j]
            if pt.symbol == t.symbol and pt.side == t.side and pt.pnl < 0:
                reason = "Same-direction add after prior position closed negative."
                flagged.append(
                    FlaggedTrade(
                        trade_index=i + 1,
                        trade=t,
                        error_class="LOSS_AVERAGING_DOWN",
                        severity="HIGH",
                        reason=reason,
                        pnl_attributed=t.pnl if t.pnl < 0 else 0,
                    )
                )
                break  # one flag per trade

    return flagged
