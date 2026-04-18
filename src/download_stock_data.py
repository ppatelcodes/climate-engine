import os
import pandas as pd
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

kite = KiteConnect(api_key = os.getenv("KITE_API_KEY"))
kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))

# Your selected companies

symbols = [
    "NTPC",
    "POWERGRID",
    "TATASTEEL",
    "JSWSTEEL",
    "ULTRACEMCO",
    "GRASIM",
    "HDFCBANK",
    "ICICIBANK",
    "TCS",
    "INFY"
]

# Load instruments file 
inst = pd.read_csv("data/raw/kite_nse_instruments.csv")

# Keep only NSE equities you need
inst = inst[inst["tradingsymbol"].isin(symbols)][["tradingsymbol", "instrument_token"]]

all_data = []

for _, row in inst.iterrows():
    symbol = row["tradingsymbol"]
    token = int(row["instrument_token"])

    print(f"Downloading {symbol}...")

    hist = kite.historical_data(
        instrument_token = token,
        from_date = "2015-01-01",
        to_date = "2025-12-31",
        interval = "day"
    )

    df = pd.DataFrame(hist)
    df["symbol"] = symbol
    all_data.append(df)

stock_df = pd.concat(all_data, ignore_index = True)
stock_df.to_csv("data/processed/stock_prices_combined.csv")

print("Saved to data/processed/stock_prices_combined.csv")
print(stock_df.head())