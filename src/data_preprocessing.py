import pandas as pd
from pathlib import Path

# Path
STOCK_FILE = "data/processed/stock_prices_combined.csv"
OUTPUT_FILE = "data/processed/stock_returns.csv"

Path("data/processed").mkdir(parents = True, exist_ok = True)

# Load stock data
df = pd.read_csv(STOCK_FILE)

print("Original shape:", df.shape)

# Convert date
df["date"] = pd.to_datetime(df["date"])

# Sort properly
df= df.sort_values(["symbol", "date"])

# Calulate daily returns
df["return"] = df.groupby("symbol")["close"].pct_change()

# Drop first NA returns
df = df.dropna(subset = ["return"])

# Add sector mapping
sector_map = {
    "NTPC": "Energy",
    "POWERGRID": "Energy",

    "TATASTEEL": "Metals",
    "JSWSTEEL": "Metals",

    "ULTRACEMCO": "Cement",
    "GRASIM": "Cement",

    "HDFCBANK": "Banking",
    "ICICIBANK": "Banking",

    "TCS": "IT",
    "INFY": "IT"
}

df["sector"] = df["symbol"].map(sector_map)

# Add useful financial metrics
# Volatility (rolling 5-day)
df["volatility_5d"] = df.groupby("symbol")["return"].rolling(5).std().reset_index(level=0, drop=True)

# Cumulative return (short-term trend)
df["cum_return_5d"] = df.groupby("symbol")["return"].rolling(5).sum().reset_index(level=0, drop=True)

# Extract NIFTY data
market = df[df["symbol"] == "NIFTY 50"][["date", "return"]].rename(
    columns = {"return": "market_return"}
)

# Merge with all stocks
df = df.merge(market, on = "date", how = "left")

# Abnormal return
df["abnormal_return"] = df["return"] - df["market_return"]

# Final dataset
final_cols = [
    "date",
    "symbol",
    "sector",
    "close",
    "return",
    "market_return",
    "abnormal_return",
    "volatility_5d",
    "cum_return_5d"
]

df = df[final_cols]

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("\n Stock preprocessing complete")
print("Final shape:", df.shape)
print("Saved to:", OUTPUT_FILE)
print("\nSample:")
print(df.head())