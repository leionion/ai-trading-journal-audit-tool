"""
Pattern aggregator — cross-trade error scoring and dollar attribution.
"""

from collections import defaultdict
from typing import List

from classifier import FlaggedTrade


def aggregate_errors(flagged: List[FlaggedTrade]) -> dict:
    """
    Aggregate flagged trades by error class with dollar attribution.
    """
    by_class: dict[str, list] = defaultdict(list)
    for f in flagged:
        by_class[f.error_class].append(f)

    summary = {}
    for cls, items in by_class.items():
        total_pnl = sum(f.pnl_attributed for f in items)
        summary[cls] = {
            "count": len(items),
            "attributed_pnl": total_pnl,
        }
    return summary
