#!/usr/bin/env python3
"""
AI Trading Journal Audit Tool — CLI entry point.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

import yaml

from parsers.base import load_and_detect
from sequencer import sequence_trades
from classifier import classify_trades
from aggregator import aggregate_errors
from session_analyzer import analyze_sessions
from report import format_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config(path: str = "config.yaml") -> dict:
    p = Path(path)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent / path
    if not p.exists():
        return {}
    with open(p) as f:
        return yaml.safe_load(f) or {}


def main():
    parser = argparse.ArgumentParser(
        description="AI Trading Journal Audit Tool — Behavioral analysis of Binance/Bybit CSV exports",
    )
    parser.add_argument("--csv", required=True, help="Path to trade history CSV")
    parser.add_argument("--exchange", choices=["binance", "bybit"], default=None, help="Exchange (auto-detect if omitted)")
    parser.add_argument("--mode", choices=["paper", "live"], default="paper", help="paper = read-only (default)")
    parser.add_argument("--config", default="config.yaml", help="Config file")
    args = parser.parse_args()

    if args.mode != "paper":
        logger.warning("Only --mode paper is supported in this build. Proceeding in paper mode.")

    config = load_config(args.config)
    if not config:
        logger.warning("Config file %s not found, using defaults", args.config)

    logger.info("Loading CSV: %s", args.csv)
    try:
        trades = load_and_detect(args.csv, args.exchange)
    except FileNotFoundError as e:
        logger.error("%s", e)
        sys.exit(1)
    except ValueError as e:
        logger.error("%s", e)
        sys.exit(1)
    if not trades:
        logger.error("No trades found in CSV")
        sys.exit(1)

    exchange_used = trades[0].exchange if trades else ""

    logger.info("Sequencing %d trades", len(trades))
    sequenced = sequence_trades(trades)

    classifier_cfg = config.get("classifier", {}) if config else {}
    logger.info("Running behavioral classifier")
    flagged = classify_trades(sequenced, classifier_cfg)

    error_summary = aggregate_errors(flagged)

    session_data = {}
    if config.get("output", {}).get("session_analysis", True):
        session_data = analyze_sessions(sequenced)

    report = format_report(sequenced, flagged, error_summary, session_data, exchange_used)

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    now = datetime.utcnow()
    ts = f"{now:%Y%m%d_%H%M%S}_{now.microsecond:06d}"
    out_path = out_dir / f"audit_report_{ts}.txt"
    with open(out_path, "w") as f:
        f.write(report)

    logger.info("Audit report written to %s", out_path)
    print(report)


if __name__ == "__main__":
    main()
