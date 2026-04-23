import os
import pandas as pd
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from pathlib import Path

load_dotenv()

kite = KiteConnect(api_key = os.getenv("KITE_API_KEY"))
kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))

# Download all NSE instruments
instruments = kite.instruments("NSE")
inst_df = pd.DataFrame(instruments)
Path("data/raw").mkdir(parents=True, exist_ok=True)

# Save
inst_df.to_csv("data/raw/kite_nse_instruments.csv", index = False)

print(inst_df[["tradingsymbol", "instrument_token", "name", "exchange"]].head())
print("Saved to data/raw/kite_nse_instruments.csv")