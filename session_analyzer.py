"""
Session timing analysis — UTC session breakdown (4-hour windows).
"""

from collections import defaultdict
from typing import List

from schema import NormalizedTrade


def analyze_sessions(trades: List[NormalizedTrade]) -> dict:
    """
    Break down performance by UTC 4-hour session windows.
    00-04, 04-08, 08-12, 12-16, 16-20, 20-24
    """
    sessions = [
        (0, 4, "00:00–04:00"),
        (4, 8, "04:00–08:00"),
        (8, 12, "08:00–12:00"),
        (12, 16, "12:00–16:00"),
        (16, 20, "16:00–20:00"),
        (20, 24, "20:00–24:00"),
    ]

    by_session: dict[str, list] = defaultdict(list)
    for t in trades:
        h = t.timestamp.hour
        for start, end, label in sessions:
            if start <= h < end:
                by_session[label].append(t)
                break

    result = {}
    for label, session_trades in by_session.items():
        if not session_trades:
            continue
        wins = sum(1 for t in session_trades if t.pnl > 0)
        total = len(session_trades)
        win_rate = 100 * wins / total if total else 0
        total_pnl = sum(t.pnl for t in session_trades)
        avg_lev = sum(t.leverage for t in session_trades) / total if total else 0
        result[label] = {
            "trades": total,
            "win_rate_pct": round(win_rate, 1),
            "total_pnl": round(total_pnl, 2),
            "avg_leverage": round(avg_lev, 1),
        }

    return result
