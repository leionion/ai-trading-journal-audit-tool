#!/usr/bin/env python3
"""Quick test for audit tool."""
import sys
sys.path.insert(0, ".")

def test_parser():
    from parsers.base import load_and_detect
    trades = load_and_detect("sample_trades_bybit.csv", "bybit")
    assert len(trades) > 0
    print(f"OK: Parsed {len(trades)} Bybit trades")

def test_binance():
    from parsers.base import load_and_detect
    trades = load_and_detect("sample_trades_binance.csv", "binance")
    assert len(trades) > 0
    print(f"OK: Parsed {len(trades)} Binance trades")

def test_audit():
    from parsers.base import load_and_detect
    from sequencer import sequence_trades
    from classifier import classify_trades
    from aggregator import aggregate_errors
    from session_analyzer import analyze_sessions
    from report import format_report

    trades = load_and_detect("sample_trades_bybit.csv", "bybit")
    sequenced = sequence_trades(trades)
    flagged = classify_trades(sequenced, {})
    summary = aggregate_errors(flagged)
    sessions = analyze_sessions(sequenced)
    report = format_report(sequenced, flagged, summary, sessions, "bybit")
    assert "AI TRADING JOURNAL AUDIT" in report
    print("OK: Full audit pipeline")
    print(report[:500] + "...")

if __name__ == "__main__":
    test_parser()
    test_binance()
    test_audit()
