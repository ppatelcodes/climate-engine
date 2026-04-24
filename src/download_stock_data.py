import os
import pandas as pd
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from pathlib import Path
from datetime import datetime, timedelta

load_dotenv()

kite = KiteConnect(api_key = os.getenv("KITE_API_KEY"))
kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))

# Selected companies

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
    "NIFTY 50"
]

# Date range
START_DATE = datetime(2015, 1, 1)
END_DATE = datetime(2025, 12, 31)

# Kite max limit per call is 2000 days
CHUNK_DAYS = 1500

# Load instruments file 
inst = pd.read_csv("data/raw/kite_nse_instruments.csv")

# Keep only NSE equities you need
inst = inst[inst["tradingsymbol"].isin(symbols)][["tradingsymbol", "instrument_token"]]

all_data = []

# Function to download in chunks
def fetch_historical_in_chunks(kite,instrument_token, start_date, end_date, interval = "day"):
    chunks = []
    current_start = start_date
    while current_start <= end_date:
        current_end = min(current_start+ timedelta(days = CHUNK_DAYS),end_date)

        print(f" Frtching {current_start.date()} to {current_end.date()}")

        hist = kite.historical_data(
            instrument_token=instrument_token,
            from_date=current_start,
            to_date=current_end,
            interval=interval
        )

        if hist:
            chunk_df = pd.DataFrame(hist)
            chunks.append(chunk_df)

        current_start = current_end + timedelta(days = 1)

    if chunks:
        return pd.concat(chunks, ignore_index = True)
    return pd.DataFrame()

# Download for each stock
for _, row in inst.iterrows():
    symbol = row["tradingsymbol"]
    token = int(row["instrument_token"])

    print(f"Downloading {symbol}...")

    stock_df = fetch_historical_in_chunks(
        kite=kite,
        instrument_token=token,
        start_date=START_DATE,
        end_date=END_DATE,
        interval="day"
    )

    if stock_df.empty:
        print(f"  No data found for {symbol}")
        continue

    stock_df["symbol"] = symbol
    all_data.append(stock_df)

# Combine and save
if all_data:
    comine_df = pd.concat(all_data, ignore_index = True)

    # Remove duplicates just in case
    combined_df = comine_df.drop_duplicates(subset = ["date","symbol"]).sort_values(["symbol","date"])

    Path("data/processed").mkdir(parents=True, exist_ok=True)

    combined_df.to_csv("data/processed/stock_prices_combined.csv", index = False)

    print("\n stock data downloaded successfully")
    print("Saved to: data/processed/stock_prices_combined.csv")
    print("Shape:", combined_df.shape)
    print(combined_df.head())
else:
    print("Noo stock data was downloaded.")