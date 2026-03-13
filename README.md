<!-- ai trading journal audit tool | ai-trading-journal-audit-tool github | leionion trading journal | trading psychology audit tool | ai trade analyzer binance bybit -->
<!-- how to detect revenge trading in trade history | how to analyze trading mistakes with AI | build trading psychology analyzer python 2026 | binance csv trade analysis python | bybit trade history psychological analysis -->
<!-- best AI trading journal crypto 2026 | trading psychology audit tool binance bybit | AI trading coach behavioral analysis | get trading journal AI analysis | crypto trade mistake detector python -->

<div align="center">

# AI Trading Journal Audit Tool

### *Your trade history already knows why you're losing. This makes it tell you.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Binance](https://img.shields.io/badge/Binance-CSV%20Native-F0B90B?style=for-the-badge&logo=binance&logoColor=black)](https://binance.com)
[![Bybit](https://img.shields.io/badge/Bybit-CSV%20Native-F7A600?style=for-the-badge&logo=bybit&logoColor=black)](https://bybit.com)
[![Status](https://img.shields.io/badge/Status-Beta%20%7C%20Shipping%20Daily-orange?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**[→ What This Does](#-what-this-actually-does) · [→ Live Audit Sample](#-live-audit-output-sample) · [→ Error Taxonomy](#-psychological-error-taxonomy) · [→ How To Run It](#-installation--setup) · [→ Full Private Build](#-want-the-full-audit-engine)**

---

> The public repo audits behavioral patterns from your CSV.
> The private build adds session-level emotion tracking, multi-exchange comparison, GPT-4o coaching prompts, and a full Streamlit dashboard.
> **Scroll to the bottom if you're serious about using it.**

</div>

---

## 🧠 What This Actually Does

Most trading journals tell you *what* happened. P&L. Win rate. Average RR.

This tool tells you *why* it happened — specifically, which cognitive and behavioral errors appear in your trade history, how often, which market conditions trigger them, and how much they cost you in dollar terms.

Drop in your **Binance or Bybit CSV export**. The tool parses every trade, sequences them chronologically, reconstructs the decision context around each one, and runs them through a psychological error classifier. You get back a structured audit report: flagged trades, error labels, severity scores, and a pattern summary.

No API keys. No account linking. No cloud upload of your trade data. **Your CSV never leaves your machine.**

```
CSV Export  →  Parser  →  Behavioral Classifier  →  Labeled Report
(your data)    (local)    (pattern detection)       (what to fix)
```

---

## 📊 Live Audit Output Sample

This is what a real audit run looks like. Input: 47 trades from a Bybit USDT-perpetual account, 14-day window.

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
| Structured psychological taxonomy | ✅ 7 classes | ❌ | ❌ | ❌ | ❌ | ❌ |
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
║              ║   (LangChain + LLM)   ║                            ║
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

Your audit report will be written to `./output/audit_report_[timestamp].txt`.

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

---

## ⚠️ Risk Disclaimer

This software is in active beta development (`v0.4.x`). It is provided for **informational and analytical purposes only**.

- This tool does **not** execute trades, connect to any exchange API, or manage funds in any way
- Behavioral pattern identification is probabilistic — classifications are AI-generated and should be reviewed critically
- **Past trade patterns do not predict future results**
- Nothing in this tool constitutes financial advice, investment advice, or a recommendation to buy or sell any asset
- Crypto derivatives trading carries substantial risk of loss, including total loss of capital
- The authors accept no liability for trading decisions made based on output from this tool
- Use paper mode (`--mode paper`) when testing to confirm expected behavior before relying on any output

---

<div align="center">

**Built with** Python · Pandas · Rich

*Because your trade history already knows the truth. This just makes it legible.*

---

</div>

<!-- get trading journal audit tool | ai trading journal full version | contact trading audit developer | leionion full build | crypto behavioral audit tool private | trading psychology analyzer full access | get ai trade analyzer binance bybit | trading journal ai private build -->
