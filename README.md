# 📊 EURUSD Microstructure Pattern Backtest

## 📌 Overview
**Python-based quantitative backtesting project** analyzing high-frequency EURUSD price data.

The project evaluates a **Fibonacci-based intraday trading pattern** using **1-minute and 2-minute candle data**, testing whether price retracements beyond the **0.618 level** generate statistically consistent outcomes.

The workflow demonstrates **data cleaning, high-performance numerical computation, vectorized backtesting, and financial performance analysis** on large-scale time-series datasets.

---

# ⚙️ Workflow

## 1️⃣ System Design
**Domain:** Forex microstructure analysis  

**Objective:**  
Test whether extreme retracement entries beyond the **0.618 Fibonacci level** provide statistically profitable short-term trades.

**Approach:**

- Use **2-minute candles** as the structural reference
- Detect entry conditions using **1-minute candle extremes**
- Evaluate trade outcomes using the **next 2-minute close**

---

# 📂 Data Source

Dataset used:

https://www.kaggle.com/datasets/ankitjha420/forex-eurusd-1m-data-2015-to-2021

The dataset contains **high-frequency EURUSD 1-minute candles** from **2015–2021**.

---

# 🧹 Data Cleaning & Preparation

Multiple CSV files were merged and cleaned using **pandas** to create a consistent dataset.

Main steps:

- Load and concatenate multiple raw CSV files
- Remove unnecessary columns
- Standardize column names
- Parse datetime values
- Remove duplicate timestamps
- Sort chronologically
- Export cleaned **1-minute dataset**
- Generate **2-minute aggregated candles**

### Cleaning Script

```python
import pandas as pd
import glob
import os

# -----------------------------------
# 1. Load all CSV files
# -----------------------------------
file_pattern = "data/*.csv"
files = glob.glob(file_pattern)

print(f"{len(files)} files detected.")

dataframes = [pd.read_csv(file) for file in files]
df = pd.concat(dataframes, ignore_index=True)

# -----------------------------------
# 2. Basic cleaning
# -----------------------------------
if "Volume" in df.columns:
    df = df.drop(columns=["Volume"])

df.columns = ["datetime", "open", "high", "low", "close"]

df["datetime"] = pd.to_datetime(
    df["datetime"],
    format="%d.%m.%Y %H:%M:%S.%f"
)

df = (
    df
    .drop_duplicates(subset="datetime")
    .sort_values("datetime")
    .reset_index(drop=True)
)

# -----------------------------------
# 3. Export 1-minute dataset
# -----------------------------------
output_1m = "EURUSD_1m_clean.csv"
df.to_csv(output_1m, index=False)

print(f"1-minute dataset saved to: {os.path.abspath(output_1m)}")

# -----------------------------------
# 4. Generate 2-minute candles
# -----------------------------------
df = df.set_index("datetime")

df_2m = (
    df
    .resample("2min")
    .agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    })
    .dropna()
    .reset_index()
)

output_2m = "EURUSD_2m_clean.csv"
df_2m.to_csv(output_2m, index=False)

print(f"2-minute dataset saved to: {os.path.abspath(output_2m)}")

print("Process completed successfully.")
```

This process generates the cleaned datasets used for the backtest:

```
EURUSD_1m_clean.csv
EURUSD_2m_clean.csv
```

---

# 🔎 Pattern Logic

The strategy detects **extreme retracement entries** relative to the previous 2-minute candle range.

### Bullish Setup

Entry triggered when price falls below:

```python
bull_entry = low - 0.618 * (high - low)
```

Trade outcome:

- **Win:** next 2-minute close ≥ entry  
- **Loss:** next 2-minute close < entry  

---

### Bearish Setup

Entry triggered when price rises above:

```python
bear_entry = high + 0.618 * (high - low)
```

Trade outcome:

- **Win:** next 2-minute close ≤ entry  
- **Loss:** next 2-minute close > entry  

---

# ⚡ High-Performance Backtesting

The backtesting engine is optimized for **large time-series datasets**.

Techniques used:

- **NumPy vectorization**
- Minimal Python loops
- Efficient memory usage
- Fast execution on hundreds of thousands of trades

Execution time for the full dataset:

```
27 seconds
```

---

# 📈 Backtest Results

| Metric | Result |
|------|------|
| Total trades | 459,541 |
| Wins | 458,687 |
| Losses | 854 |
| Win rate | 99.81% |
| Total profit (units) | 457,833 |
| Profit per hour | 8.70 |
| Standard deviation | 0.45 |
| Maximum drawdown | -6 |
| Max win streak | 2,159 |
| Max loss streak | 3 |

---

# 📉 Equity Curve

The backtest exports the full equity progression for further analysis:

```
equity_curve.csv
```

Columns:

| Column | Description |
|------|------|
| trade_index | sequential trade number |
| result | trade outcome (1 = win, -1 = loss) |
| equity | cumulative profit |

This dataset can be used for:

- equity curve visualization
- drawdown analysis
- further statistical evaluation

---

# 🛠️ How to Run

### 1️⃣ Prepare Data

Place raw CSV files in the `data` folder.

### 2️⃣ Run the cleaning pipeline

```
python clean_data.py
```

This will generate:

```
EURUSD_1m_clean.csv
EURUSD_2m_clean.csv
```

### 3️⃣ Run the backtest

```
python backtest.py
```

Outputs:

```
equity_curve.csv
console performance metrics
```

---

# 🚀 Key Skills Demonstrated

| Skill | Application |
|------|------|
| Quantitative Finance | Trading strategy backtesting |
| High-frequency data analysis | Forex candle microstructure |
| Data engineering | Large CSV ingestion and cleaning |
| Python performance optimization | NumPy vectorization |
| Financial metrics | drawdown, winrate, streak analysis |
| Reproducible workflows | modular data pipeline |

---

💡 **Portfolio Note**

This project demonstrates the ability to **clean large financial datasets, design rule-based trading systems, and implement high-performance backtesting pipelines in Python.**
