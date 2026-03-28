# 📈 EURUSD High-Frequency Data Pipeline & Pattern Analysis

> End-to-end quantitative research pipeline built in Python — from raw multi-file Forex data to vectorized pattern detection and statistical validation across 6 years of 1-minute OHLC candles.

---

## 🗂️ Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Key Findings](#key-findings)
- [Workflow](#workflow)
- [Pattern Logic](#pattern-logic)
- [Statistical Results](#statistical-results)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)

---

## Overview

This project applies a **full quantitative research workflow** to high-frequency Forex data (EURUSD, 2015–2021).

The objective was to design, implement, and statistically validate a price action hypothesis using **Python, pandas, and NumPy** — processing millions of rows efficiently through vectorized computation.

The pipeline covers every stage of a real data analysis project:

- **Data engineering:** merging, cleaning, and aggregating multi-file time-series CSVs
- **Feature engineering:** constructing candle anatomy metrics from raw OHLC values
- **Hypothesis testing:** evaluating a directional pattern across 81,000+ observations
- **Statistical reporting:** computing win rate, profit factor, expectancy, and variance

This workflow mirrors the kind of **reproducible, scalable analysis** used in financial data science, product analytics, and quantitative research environments.

---

## Tech Stack

| Layer | Tool / Library |
|---|---|
| Data Processing | Python, pandas |
| Numerical Computation | NumPy (vectorized) |
| Time-Series Engineering | pandas datetime, resampling |
| Statistical Reporting | Custom backtesting engine |
| Dataset | [Kaggle – EURUSD 1m 2015–2021](https://www.kaggle.com/datasets/ankitjha420/forex-eurusd-1m-data-2015-to-2021) |

---

## Key Findings

| Metric | Value |
|---|---|
| Total Observations | 81,938 |
| Pattern Occurrences (Signals) | 81,938 |
| Win Rate | 51.15% |
| Profit Factor | 1.047 |
| Expectancy | +0.023 per trade unit |
| Std Deviation | 0.9997 |

**Statistical interpretation:**

The pattern produces a **slight but consistent positive bias** across the full 6-year dataset. With 81k+ independent observations, even a marginal deviation from 50% is statistically meaningful — random noise at this sample size would produce a near-perfect 50.0% split.

The results suggest the candle structure captures a **weak but real microstructure signal**, providing a solid foundation for further research with additional filters (session, volatility regime, spread modeling).

---

## Workflow

### 1. Data Collection

- Source: EURUSD 1-minute OHLC candles from Kaggle (2015–2021)
- Multi-file CSV format requiring merging and standardization
- Higher timeframe reconstruction (2-minute candles) built from 1-minute base data

### 2. Data Cleaning Pipeline

Raw CSV files processed through a structured pandas pipeline:

```
✔ Merge multiple CSV files into a single dataset
✔ Drop redundant columns
✔ Standardize column names and data types
✔ Parse and validate datetime index
✔ Remove duplicate timestamps
✔ Sort chronologically
✔ Export EURUSD_1m_clean.csv
✔ Resample and export EURUSD_2m_clean.csv
```

### 3. Feature Engineering

For each 2-minute candle, derived metrics are computed:

```python
body        = abs(close - open)
upper_wick  = high - max(close, open)
lower_wick  = min(close, open) - low
```

These features allow pattern matching without any external indicators — purely structural candle analysis.

### 4. Pattern Detection

The algorithm scans every 2-minute candle for a **momentum structure with limited retracement**:

See [Pattern Logic](#pattern-logic) section below.

### 5. Backtesting Engine

A custom **NumPy-based engine** processes all signals in vectorized form — no Python loops over rows.

Key design decisions:
- Vectorized array operations for speed and memory efficiency
- Limit order simulation: entry at candle open via 1-minute retracement check
- Outcome evaluation: close of the following 2-minute candle
- Automatic export of results to `backtest_results.txt`

---

## Pattern Logic

The strategy identifies **momentum candles with limited wick retracement** — candles where price moved strongly with minimal pullback, breaking the prior candle's range.

### Bullish Signal Conditions

```python
close > open                    # Bullish candle
upper_wick < body               # Limited upper retracement
close > previous_high           # Range breakout confirmation
```

### Bearish Signal Conditions

```python
close < open                    # Bearish candle
lower_wick < body               # Limited lower retracement
close < previous_low            # Range breakout confirmation
```

After signal detection, **1-minute data is used to check for a retracement to the candle open** — simulating a limit order entry rather than a market order. This makes the backtest more realistic by avoiding fill-at-close assumptions.

---

## Statistical Results

| Metric | Value | Interpretation |
|---|---|---|
| Trades | 81,938 | Large sample — statistically robust |
| Win Rate | 51.15% | Slight positive bias above chance |
| Profit Factor | 1.047 | Revenue > cost at 1:1 risk |
| Expectancy | +0.023 | Positive expected value per trade |
| Std Deviation | 0.9997 | High variance — signal is weak |

**Limitations and next steps:**

- Transaction costs and spread not yet modeled
- No volatility regime filtering (high-impact news events inflate noise)
- Session-based segmentation (London/New York) could improve signal clarity
- Multi-candle confirmation logic could reduce false positives

---

## Project Structure

```
Trading-Profit-Patterns/
│
├── data/
│   ├── lua/                    
│   ├── candle_pattern.lua        
│
├── patterns/
│   ├── downward_pattern.png     
│   ├── upward_pattern.png
├── python/
│   ├── backtest.py     
│   ├── eurusd_data_merger.py       
│
└── README.md
```

---

## How to Run

**1. Download the dataset**

[EURUSD 1m 2015–2021 on Kaggle](https://www.kaggle.com/datasets/ankitjha420/forex-eurusd-1m-data-2015-to-2021)

Place raw CSV files inside `data/raw/`.

**2. Run the cleaning pipeline**

```bash
python src/clean_data.py
```

Outputs: `EURUSD_1m_clean.csv`, `EURUSD_2m_clean.csv`

**3. Run the backtest**

```bash
python src/backtest_numpy.py
```

Output: `backtest_results.txt`

---

## What This Project Demonstrates

| Skill | Application |
|---|---|
| Data Engineering | Multi-file CSV merging, cleaning, and time-series resampling |
| Feature Engineering | Deriving candle structure metrics from raw OHLC |
| Vectorized Computing | NumPy-based processing of millions of rows |
| Hypothesis Testing | Statistical validation of a price action pattern |
| Quantitative Thinking | Interpreting win rate, profit factor, and expectancy |
| Reproducibility | Structured pipeline with exported datasets and reports |

---

*Analysis by [Santiago Acosta](https://github.com/santiagoacostab17)*
