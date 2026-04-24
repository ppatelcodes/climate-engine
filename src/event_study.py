import pandas as pd
from pathlib import Path

CLIMATE_FILE = "data/processed/climate_events_clean.csv"
STOCK_FILE = "data/processed/stock_returns.csv"

EVENT_OUTPUT = "data/processed/event_study_results.csv"
SECTOR_OUTPUT = "data/processed/sector_event_impact.csv"

Path("data/processed").mkdir(parents=True, exist_ok=True)

# Load data
climate = pd.read_csv(CLIMATE_FILE)
stocks = pd.read_csv(STOCK_FILE)

# Fix dates properly
climate["event_date"] = pd.to_datetime(climate["event_date"]).dt.tz_localize(None)
stocks["date"] = pd.to_datetime(stocks["date"], utc=True).dt.tz_convert(None).dt.normalize()

# Remove bad rows
stocks = stocks.dropna(subset=["date", "symbol", "sector", "return"])
climate = climate.dropna(subset=["event_date"])

print("Climate rows:", climate.shape)
print("Stock rows:", stocks.shape)
print("Stock date range:", stocks["date"].min(), "to", stocks["date"].max())
print("Climate date range:", climate["event_date"].min(), "to", climate["event_date"].max())

PRE_DAYS = 5
POST_DAYS = 5

results = []

for _, event in climate.iterrows():
    raw_event_date = event["event_date"]

    for symbol in stocks["symbol"].unique():
        stock_df = stocks[stocks["symbol"] == symbol].sort_values("date").reset_index(drop=True)

        if stock_df.empty:
            continue

        # Find nearest trading day index
        nearest_idx = (stock_df["date"] - raw_event_date).abs().idxmin()

        start_idx = max(nearest_idx - PRE_DAYS, 0)
        end_idx = min(nearest_idx + POST_DAYS, len(stock_df) - 1)

        before = stock_df.iloc[start_idx:nearest_idx]
        after = stock_df.iloc[nearest_idx:end_idx + 1]

        if before.empty or after.empty:
            continue

        avg_return_before = before["return"].mean()
        avg_return_after = after["return"].mean()

        impact = avg_return_after - avg_return_before

        results.append({
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "raw_event_date": raw_event_date,
            "aligned_trading_date": stock_df.loc[nearest_idx, "date"],
            "location": event["location"],
            "severity_level": event["severity_level"],
            "severity_score": event["severity_score"],
            "symbol": symbol,
            "sector": stock_df.loc[nearest_idx, "sector"],
            "avg_return_before": avg_return_before,
            "avg_return_after": avg_return_after,
            "impact": impact
        })

event_results = pd.DataFrame(results)

if event_results.empty:
    raise ValueError("No event study results generated. Check stock symbols, dates, and climate file.")

event_results.to_csv(EVENT_OUTPUT, index=False)

sector_summary = (
    event_results
    .groupby(["sector", "event_type"], as_index=False)
    .agg(
        events_analyzed=("event_id", "count"),
        avg_impact=("impact", "mean"),
        avg_severity_score=("severity_score", "mean")
    )
    .sort_values("avg_impact")
)

sector_summary.to_csv(SECTOR_OUTPUT, index=False)

print("\nEvent study complete")
print("Saved:", EVENT_OUTPUT)
print("Saved:", SECTOR_OUTPUT)

print("\nEvent results shape:", event_results.shape)
print(event_results[["event_type", "symbol", "sector", "avg_return_before", "avg_return_after", "impact"]].head())

print("\nSector summary:")
print(sector_summary.head())