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
