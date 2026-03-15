<div align="center">

# AI Trading Journal Audit Tool

### Analyze Binance and Bybit trading journal CSV files to detect behavioral trading mistakes

> Local-first trading journal analyzer for identifying revenge trading, overleverage, FOMO entries, session weakness, and other costly trading patterns from your CSV history.

</div>

---

![Audit demo — live console output](media.gif)

## What This Project Does

AI Trading Journal Audit Tool is a **trading journal analyzer** for **Binance** and **Bybit** CSV exports.

Most trading journals show basic metrics like win rate, profit and loss, or average risk-reward. This tool goes further by identifying **behavioral trading mistakes** and showing which patterns are damaging performance.

It reads your trade history, reconstructs trade sequences, detects repeated error patterns, and generates an audit report with:

- flagged trades
- behavioral error labels
- severity scores
- session-based performance analysis
- estimated dollar cost by error type

This project is built for:

- crypto traders reviewing their own performance
- discretionary traders trying to reduce emotional mistakes
- trading coaches and educators
- developers building trading psychology or journaling products

**Everything runs locally.**  
No exchange account linking, no cloud upload, and no requirement to send trading data to external services.

Below is the text report format. The example shows a larger run; the bundled sample CSVs produce shorter reports.

```
═══════════════════════════════════════════════════════════════════
  AI TRADING JOURNAL AUDIT — REPORT v0.4.1
  Account Snapshot: BYBIT_USDT_PERP | Period: 2026-02-14 → 2026-02-28
  Trades Analyzed: 47 | Flagged: 19 (40.4%) | Generated: 2026-02-28 14:32 UTC
═══════════════════════════════════════════════════════════════════

PSYCHOLOGICAL ERROR BREAKDOWN
──────────────────────────────────────────────────────────────────
  REVENGE_TRADING        ██████████░░░░  8 instances  |  -$412.50 attributed
  OVERLEVERAGE           ████████░░░░░░  6 instances  |  -$318.00 attributed
  FOMO_ENTRY             █████░░░░░░░░░  4 instances  |  -$174.20 attributed
  LOSS_AVERAGING_DOWN    ██░░░░░░░░░░░░  1 instance   |  -$89.00  attributed
──────────────────────────────────────────────────────────────────
  TOTAL BEHAVIORAL COST  19 flagged trades             |  -$993.70 attributed

FLAGGED TRADE DETAIL (Top 5 by severity)
──────────────────────────────────────────────────────────────────
  [CRITICAL] Trade #31  |  2026-02-21 03:17 UTC
  Pair: SOLUSDT | Side: LONG | Size: 18x leverage | PnL: -$214.00
  Error: REVENGE_TRADING
  Reason: Entry placed 4 minutes after Trade #30 closed at -$108.00.
          Position size increased 3.2x vs prior trade. Classic
          loss-recovery escalation pattern detected.
  ──────────────────────────────────────────────────────────────
  [HIGH]     Trade #38  |  2026-02-24 11:44 UTC
  Pair: ETHUSDT | Side: SHORT | Size: 25x leverage | PnL: -$189.00
  Error: OVERLEVERAGE
  Reason: 25x on a position sized 18% of account equity. Leverage
          exceeded your 14-day personal median (8x) by 212%.
          No stop-loss detected in export metadata.
  ──────────────────────────────────────────────────────────────
  [HIGH]     Trade #12  |  2026-02-17 20:58 UTC
  Pair: BTCUSDT | Side: LONG | Size: 10x leverage | PnL: -$97.20
  Error: FOMO_ENTRY
  Reason: Entry at local 4H high following a 6.2% candle. Price had
          already moved; entry places you at maximum extension.
          No retracement or consolidation confirmation detected.
  ──────────────────────────────────────────────────────────────

PATTERN SUMMARY
──────────────────────────────────────────────────────────────────
  Primary driver of losses: Revenge trading loop after drawdown
  Trigger condition:        Back-to-back losses within 2-hour window
  Risk escalation:          You increase position size after losses,
                            not after wins — inverse of healthy sizing
  Safest session:           UTC 08:00–12:00 (London open) — 71% win rate
  Most destructive session: UTC 00:00–04:00 — 23% win rate, highest avg leverage

RECOMMENDATION
──────────────────────────────────────────────────────────────────
  Rule to implement: Hard stop after 2 consecutive losses in any
  4-hour window. Mandatory 90-minute cooldown before re-entry.
  Projected impact: Eliminates 8 of 19 flagged trades ($412.50).

═══════════════════════════════════════════════════════════════════
```

---

## 🔬 Psychological Error Taxonomy

The agent classifies trades against a structured taxonomy built specifically for crypto derivatives trading. These are not generic labels — each has a precise, measurable detection signature.

| Error Class | Detection Signature | Common Trigger |
|---|---|---|
| `REVENGE_TRADING` | Entry < 10 min after loss + position size increase ≥ 1.5x | Consecutive losses in same session |
| `OVERLEVERAGE` | Leverage > 2x personal 14-day median AND > 15% equity per trade | High-volatility breakout moves |
| `FOMO_ENTRY` | Entry at or above N-period high after ≥ 4% candle with no pullback | Viral price moves, Twitter/CT pumps |
| `LOSS_AVERAGING_DOWN` | Same-direction add-on after open position goes negative ≥ 5% | Strong trend against position |
| `PREMATURE_EXIT` | Exit before TP with ≥ 60% of target achieved, trade would have hit TP | Recent losing streak causing fear |
| `OVERTRADING` | > 3x personal daily trade average with no increase in win rate | Slow market / boredom / drawdown |
| `POSITION_SIZE_CHAOS` | Standard deviation of position sizes > 80% of mean over 7-day window | Emotional state volatility |

---

## ⚔️ How This Compares to Every Alternative You've Tried

| | AI Trading Journal Audit Tool | TraderSync | Tradervue | Notion Template | Manual Spreadsheet | Generic ChatGPT |
|---|---|---|---|---|---|---|
| Reads Binance/Bybit CSV directly | ✅ | ✅ (paid) | ✅ (limited) | ❌ manual | ❌ manual | ❌ no structure |
| AI behavioral error detection | ✅ | ❌ stats only | ❌ stats only | ❌ | ❌ | ⚠️ inconsistent |
| Detects revenge trading specifically | ✅ | ❌ | ❌ | ❌ | ❌ | ⚠️ if prompted right |
| Session-timing analysis | ✅ | ⚠️ basic | ⚠️ basic | ❌ | ❌ | ❌ |
| Dollar cost per error type | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| No account linking required | ✅ | ❌ OAuth | ❌ OAuth | ✅ | ✅ | ✅ |
| Data stays local (no cloud) | ✅ | ❌ SaaS | ❌ SaaS | ✅ | ✅ | ❌ OpenAI |
| Structured psychological taxonomy | ✅ 4 classes (7 in roadmap) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Monthly cost** | **$0** | **$29.95/mo** | **$29.95/mo** | **$0** | **$0** | **~$20/mo** |

---

## 🏗️ System Architecture

```
╔══════════════════════════════════════════════════════════════════╗
║                  AI TRADING JOURNAL AUDIT TOOL                   ║
╠══════════════╦═══════════════════════╦════════════════════════════╣
║  INPUT LAYER ║   AGENT CORE          ║   OUTPUT LAYER             ║
║              ║                       ║                            ║
║  Binance CSV ╠══► CSV Parser         ║   audit_report.txt         ║
║  Bybit CSV   ║    (normalize schema) ║   flagged_trades.json      ║
║              ║         │             ║   error_summary.csv        ║
║              ║         ▼             ║                            ║
║              ║   Trade Sequencer     ║   [Full Build Only]        ║
║              ║   (chronological +    ║   Streamlit Dashboard      ║
║              ║    context windows)   ║   PDF Audit Report         ║
║              ║         │             ║   GPT-4o Coach Prompts     ║
║              ║         ▼             ║   Multi-session Heatmap    ║
║              ║   Behavioral          ║                            ║
║              ║   Classifier Agent    ║                            ║
║              ║   (rule-based; LLM    ║                            ║
║              ║    in full build)      ║                            ║
║              ║         │             ║                            ║
║              ║         ▼             ║                            ║
║              ║   Pattern Aggregator  ║                            ║
║              ║   (cross-trade        ║                            ║
║              ║    error scoring)     ║                            ║
╚══════════════╩═══════════════════════╩════════════════════════════╝
  No API keys.   Runs locally.   Your CSV never touches a server.
```

---

## ⚙️ Installation & Setup

**Step 1 — Clone the repository**
```bash
git clone https://github.com/leionion/ai-trading-journal-audit-tool.git
cd ai-trading-journal-audit-tool
```

**Step 2 — Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Step 3 — (Optional) Configure LLM in `.env` for future enrichment**
```bash
cp .env.example .env
# The beta uses rule-based classification — no API key required.
# .env is for future LLM-backed features (v0.5.1+).
```

**Step 4 — Export your trade history CSV**
- **Binance:** Account → Order History → Export → Select date range → Download CSV
- **Bybit:** My Assets → Order History → Export → Trade Records → Download

**Step 5 — Run the audit (paper mode — read only, no live connection)**
```bash
python audit.py --csv your_trades.csv --exchange binance --mode paper
# Or omit --exchange to auto-detect from CSV headers
```

Your audit report will be written to `./output/audit_report_YYYYMMDD_HHMMSS_microseconds.txt` (unique per run).

**Try with sample data:**
```bash
python audit.py --csv sample_trades_bybit.csv --exchange bybit --mode paper
python audit.py --csv sample_trades_binance.csv --exchange binance --mode paper
```

---

## 🔧 Configuration Reference

```yaml
# config.yaml — full configuration reference

# ── LLM Settings ──────────────────────────────────────────────────
llm:
  provider: openai          # openai | anthropic | ollama | groq
  model: gpt-4o-mini        # gpt-4o-mini is sufficient; gpt-4o for higher accuracy
  temperature: 0.1          # keep low — you want deterministic classifications
  max_tokens: 2000

# ── Behavioral Classifier Settings ────────────────────────────────
classifier:
  revenge_trading_window_minutes: 10    # time window to check for loss→entry pattern
  overleverage_median_multiplier: 2.0   # triggers if leverage > 2x personal 14d median
  fomo_candle_threshold_pct: 4.0        # entry after X% candle with no pullback
  min_trades_for_pattern: 3             # minimum trades before pattern-level flagging

# ── Exchange Schema ────────────────────────────────────────────────
exchange:
  name: binance             # binance | bybit
  instrument_type: futures  # futures | spot
  currency: USDT

# ── Output Settings ────────────────────────────────────────────────
output:
  format: text              # text | json | both
  include_raw_flags: true   # include per-trade detection reasoning
  dollar_attribution: true  # calculate PnL attributed to each error class
  session_analysis: true    # break down performance by UTC session
```

---

## 🗺️ Roadmap

### ✅ Shipped
- `v0.1.0` — Binance CSV parser + trade sequencer
- `v0.2.0` — Core behavioral classifier (4 error classes)
- `v0.3.0` — Bybit CSV support + schema normalization
- `v0.4.0` — Pattern aggregator + dollar attribution per error class
- `v0.4.1` — Session timing analysis (UTC session breakdown)

### 🔨 Active Development
- `v0.5.0` — Full 7-class error taxonomy (3 new classes)
- `v0.5.1` — Groq and Ollama LLM backend support (fully local, zero API cost)
- `v0.5.2` — JSON + CSV output formats alongside text report

### 🔜 Planned (Private Build)
- `v0.6.0` — Streamlit dashboard with interactive trade timeline
- `v0.7.0` — Multi-session heatmap (performance by day/hour grid)
- `v0.8.0` — GPT-4o coaching prompt generator (personalized to your error profile)
- `v0.9.0` — OKX and Hyperliquid CSV support
- `v1.0.0` — PDF audit report export + shareable summary card

---

## 🔒 Want the Full Audit Engine?

The public build gives you the core classifier. Serious traders who want the complete system — dashboard, coaching prompts, heatmaps, and full 7-class taxonomy — reach out directly.

**This is built for:**

| Profile | What You Get |
|---|---|
| Retail trader losing > $500/month to behavioral errors | The full report shows exactly which errors to eliminate first — highest ROI fix identified by dollar impact |
| Trader who's profitable but inconsistent | Pattern analysis reveals which sessions and market conditions destabilize your edge, and which to double down on |
| Developer building a prop firm or trading education platform | The classifier engine and taxonomy are available for integration — structured output, clean API |
| Quant / algo trader reviewing discretionary override decisions | Behavioral audit of manual interventions against your systematic signals — quantify how much your gut costs you |

**How to reach me:**

→ GitHub: **[github.com/leionion](https://github.com/leionion)**
→ Open a GitHub Discussion or drop a note on any issue

**When you reach out, mention:**
1. Which exchange you trade on and roughly how many trades per month
2. Whether you want the full personal audit build or the developer/integration version
3. The single biggest pattern you already suspect in your own trading

The gap between this public build and the private one isn't a matter of time — it's a feature gap that's intentional. The full version surfaces the things most traders don't want to see. That's exactly why it works.
