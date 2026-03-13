"""
Trade sequencer — chronological ordering and context windows.
"""

from typing import List

from schema import NormalizedTrade


def sequence_trades(trades: List[NormalizedTrade]) -> List[NormalizedTrade]:
    """
    Sort trades chronologically and assign 1-based indices for reporting.
    """
    sorted_trades = sorted(trades, key=lambda t: t.timestamp)
    return sorted_trades
