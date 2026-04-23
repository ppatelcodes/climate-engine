import pandas as pd
from pathlib import Path

# Paths
CLIMATE_FILE = "data/processed/climate_events_clean.csv"
STOCK_FILE = "data/processed/stock_returns.csv"

EVENT_OUTPUT = "data/processed/event_study_results.csv"
SECTOR_OUTPUT = "data/processed/sector_event_impact.csv"

Path("data/processed").mkdir(parents=True, exist_ok=True)

# Load data
climate = pd.read_csv(CLIMATE_FILE)
stocks = pd.read_csv(STOCK_FILE)

# Convert dates
climate["event_date"] = climate["event_date"].astype(str).str.strip()
climate["event_date"] = pd.to_datetime(climate["event_date"], errors = "coerce")

stocks["date"] = stocks["date"].astype(str).str.strip()
stocks["date"] = pd.to_datetime(stocks["date"], errors = "coerce")

# Remove timezone (IMPORTANT)
stocks["date"] = stocks["date"].dt.tz_localize(None)

# Drop bad rows if any
climate = climate.dropna(subset=["event_date"]).copy()
stocks = stocks.dropna(subset=["date"]).copy()

print("Climate shape:", climate.shape)
print("Stock shape:", stocks.shape)
print("Climate event_date dtype:", climate["event_date"].dtype)
print("Stocks date dtype:", stocks["date"].dtype)

# event study parameters
PRE_EVENT_DAYS = 5
POST_EVENT_DAYS = 5

results = []

# Loop through each climate event
for _, event in climate.iterrows():
    event_id = event["event_id"]
    event_type = event["event_type"]
    event_date = pd.to_datetime(event["event_date"], errors="coerce")
    location = event["location"]
    severity_level = event["severity_level"]
    severity_score = event["severity_score"]

    if pd.isna(event_date):
        continue

    # Window selection 
    window_data = stocks[
        (stocks["date"] >= (event_date - pd.Timedelta(days = PRE_EVENT_DAYS))) &
        (stocks["date"] <= (event_date + pd.Timedelta(days = POST_EVENT_DAYS)))
    ].copy()

    if window_data.empty:
        continue

    # Seperate before and after event windows
    before_data = window_data[window_data["date"] < event_date]
    after_data = window_data[window_data["date"] >= event_date]

    # Group by stock symbol
    for symbol in window_data["symbol"].unique():
        stock_before = before_data[before_data["symbol"] == symbol]
        stock_after = after_data[after_data["symbol"] == symbol]
        stock_all = window_data[window_data["symbol"] == symbol]

        # Skip if insufficient data
        if stock_before.empty or stock_after.empty:
            continue

        sector = stock_all["sector"].iloc[0]

        avg_return_before = stock_before["return"].mean()
        avg_return_after = stock_after["return"].mean()

        avg_vol_before = stock_before["volatility_5d"].mean()
        avg_vol_after = stock_after["volatility_5d"].mean()

        impact = avg_return_after - avg_return_before
        volatility_change = avg_vol_after - avg_vol_before

        results.append({
            "event_id": event_id,
            "event_type": event_type,
            "event_date": event_date,
            "location": location,
            "severity_level": severity_level,
            "severity_score": severity_score,
            "symbol": symbol,
            "sector": sector,
            "avg_return_before": avg_return_before,
            "avg_return_after": avg_return_after,
            "impact": impact,
            "avg_volatility_before": avg_vol_before,
            "avg_volatility_after": avg_vol_after,
            "volatility_change": volatility_change
        })

# Create event study dataframe
event_results = pd.DataFrame(results)

if event_results.empty:
    print("No event study results generated. Check date overlap between climate and stock data.")
else:
    # Sort nicely
    event_results = event_results.sort_values(["event_date", "symbol"]).reset_index(drop = True)

    # Save detailed results
    event_results.to_csv(EVENT_OUTPUT, index = False)

    print("\n event study file created")
    print("Saved to:", EVENT_OUTPUT)
    print("Shape:", event_results.shape)

    # Sector level summary
    sector_summary = (
        event_results.groupby(["sector","event_type"], as_index = False).agg(
            events_analyzed = ("event_id", "count"),
            avg_impact = ("impact", "mean"),
            avg_volatility_change = ("volatility_change","mean"),
            avg_severity_score = ("severity_score", "mean")
        )
        .sort_values(["avg_impact"])
        .reset_index(drop = True)
    )

    sector_summary.to_csv(SECTOR_OUTPUT, index = False)

    print("\n Sector summary file created")
    print("Sector output saved to:", SECTOR_OUTPUT)
    print("\n Sample detailed results:")
    print(event_results.head())
    print("\n Sample sector summary:")
    print(sector_summary.head())