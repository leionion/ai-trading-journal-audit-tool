"""
Report formatter — produces audit_report.txt matching README sample.
"""

from datetime import datetime
from typing import List

from classifier import FlaggedTrade
from schema import NormalizedTrade


def _max_bar() -> int:
    return 14


def _bar_chart(count: int, max_count: int) -> str:
    if max_count <= 0:
        return "░░░░░░░░░░░░░░"
    filled = int((count / max_count) * _max_bar())
    return "█" * filled + "░" * (_max_bar() - filled)


def format_report(
    trades: List[NormalizedTrade],
    flagged: List[FlaggedTrade],
    error_summary: dict,
    session_data: dict,
    exchange: str = "",
) -> str:
    """
    Produce text report matching README sample format.
    """
    period_start = min(t.timestamp for t in trades) if trades else datetime.utcnow()
    period_end = max(t.timestamp for t in trades) if trades else datetime.utcnow()

    exchange_label = f"{exchange.upper()}_USDT_PERP" if exchange else "UNKNOWN"
    total_flagged = len(flagged)
    total_trades = len(trades)
    pct = 100 * total_flagged / total_trades if total_trades else 0
    total_cost = sum(f.pnl_attributed for f in flagged)

    lines = [
        "═" * 67,
        "  AI TRADING JOURNAL AUDIT — REPORT v0.4.1",
        f"  Account Snapshot: {exchange_label} | Period: {period_start.strftime('%Y-%m-%d')} → {period_end.strftime('%Y-%m-%d')}",
        f"  Trades Analyzed: {total_trades} | Flagged: {total_flagged} ({pct:.1f}%) | Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
        "═" * 67,
        "",
        "PSYCHOLOGICAL ERROR BREAKDOWN",
        "─" * 67,
    ]

    max_count = max((s["count"] for s in error_summary.values()), default=1)
    for cls, data in sorted(error_summary.items(), key=lambda x: -x[1]["count"]):
        bar = _bar_chart(data["count"], max_count)
        inst = "instance" if data["count"] == 1 else "instances"
        ap = data["attributed_pnl"]
        pnl_str = f"-${abs(ap):,.2f}" if ap < 0 else f"${ap:,.2f}"
        lines.append(f"  {cls:24} {bar}  {data['count']} {inst:8} |  {pnl_str} attributed")
    lines.append("─" * 67)
    cost_str = f"-${abs(total_cost):,.2f}" if total_cost < 0 else f"${total_cost:,.2f}"
    lines.append(f"  TOTAL BEHAVIORAL COST  {total_flagged} flagged trades             |  {cost_str} attributed")
    lines.append("")
    lines.append("FLAGGED TRADE DETAIL (Top 5 by severity)")
    lines.append("─" * 67)

    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    top5 = sorted(flagged, key=lambda f: (sev_order.get(f.severity, 4), -abs(f.pnl_attributed)))[:5]
    for f in top5:
        t = f.trade
        lines.append(f"  [{f.severity:8}] Trade #{f.trade_index}  |  {t.timestamp.strftime('%Y-%m-%d %H:%M')} UTC")
        pnl_fmt = f"-${abs(t.pnl):,.2f}" if t.pnl < 0 else f"${t.pnl:,.2f}"
        lines.append(f"  Pair: {t.symbol} | Side: {t.side} | Size: {t.leverage:.0f}x leverage | PnL: {pnl_fmt}")
        lines.append(f"  Error: {f.error_class}")
        lines.append(f"  Reason: {f.reason}")
        lines.append("  ─────────────────────────────────────────────────────────")
    lines.append("")
    lines.append("PATTERN SUMMARY")
    lines.append("─" * 67)

    if error_summary:
        top_error = max(error_summary.items(), key=lambda x: x[1]["count"])
        lines.append(f"  Primary driver of losses: {top_error[0].replace('_', ' ').lower()}")
    else:
        lines.append("  Primary driver of losses: (no flagged trades)")
    lines.append("  Trigger condition:        Consecutive losses or leverage spikes")
    lines.append("  Risk escalation:         Review position sizing after losses")
    if session_data:
        best = max(session_data.items(), key=lambda x: (x[1]["win_rate_pct"], x[1]["total_pnl"]))
        worst_cands = [(k, v) for k, v in session_data.items() if k != best[0]]
        worst = min(worst_cands, key=lambda x: (x[1]["win_rate_pct"], x[1]["total_pnl"])) if worst_cands else best
        lines.append(f"  Safest session:           {best[0]} — {best[1]['win_rate_pct']}% win rate")
        if best[0] == worst[0]:
            lines.append(f"  Most destructive session: {worst[0]} — {worst[1]['win_rate_pct']}% win rate (single session with trades)")
        else:
            lines.append(f"  Most destructive session: {worst[0]} — {worst[1]['win_rate_pct']}% win rate, highest avg leverage")
    else:
        lines.append("  Safest session:           (insufficient trades for session analysis)")
    lines.append("")
    lines.append("RECOMMENDATION")
    lines.append("─" * 67)
    lines.append("  Rule to implement: Hard stop after 2 consecutive losses in any")
    lines.append("  4-hour window. Mandatory 90-minute cooldown before re-entry.")
    if total_flagged > 0:
        lines.append(f"  Projected impact: Eliminates {min(total_flagged, 8)} of {total_flagged} flagged trades (${abs(total_cost):,.2f}).")
    lines.append("")
    lines.append("═" * 67)
    return "\n".join(lines)
