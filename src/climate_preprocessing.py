import pandas as pd
import numpy as np
from pathlib import pathlib

# Paths
INPUT_FILE = "data/raw/emdat_india.xlsx"
OUTPUT_FILE = "data/processed/climate_events_clean.csv"

# Makek sure output folder exists
Path("data/processed").mkdir(parents = True, exist_ok = True)

# Load data
df = pd.read_excel(INOUT_FILE)

print("Original shape:", df.shape)
print("Columns loaded successfully.\n")

# Keep only India data
df = df[df["Country"] == "India"].copy()
print("After filtering India data:", df.shape)

# Keep onlt relevant disaster types
valid_events == [
    "Flood",
    "Storm",
    "Drought",
    "Extreme temperature",
    "Glacial lake outburst flood"
]

df =df[df["Disaster Type"].isin(valid_events)].copy()
print("After filtering relevant climate events:", df.shape)

# Create proper event start date
df["Start Month"] = df["Start Month"].fillna(1)
df["Start Day"] = df["Start Day"].fillna(1)

df["event_date"] = pd.to_datetime(
 df["Start Year"].astype(int).astype(str) + "-" +
 df["Start Month"].astype(int).astype(str) + "-" +
 df["Start Day"].astype(int).astype(str),
 errors = "coerce"   
)

# Create end date too 
df["End Month"] = df["End Month"].fillna(df["Start Month"])
df["End Day"] = df["End Day"].fillna(df["Start Day"])

df["end_date"] = pd.to_datetime(
    df["End Year"].fillna(df["Start Year"]).astype(int).astype(str) + "-" +
    df["End Month"].astype(int).astype(str) + "-" +
    df["End Day"].astype(int).astype(str),
    errors="coerce"
)

# Create severity_score
df["Total Damage ('000 US$)"] = pd.to_numeric(df["Total Damage ('000 US$)"], error = "coerce")
df["Total Affected"] = pd.to_numeric(df["Total Affected"], error = "coerce")
df["Total Deaths"] = pd.to_numeric(df["Total Deaths"], error = "coerce")
df["Magnitude"] = pd.to_numeric(df["Magnitude"], error = "coerce")

df["severity_score"] = df["Total Damage ('000 US$)"]
df["severity_score"] = df["severity_score"].fillna(df["Total Affected"])
df["severity_score"] = df["severity_score"].fillna(df["Total Deaths"])
df["severity_score"] = df["severity_score"].fillna(df["Magnitude"])
df["severity_score"] = df["severity_score"].fillna(0)

# Create severity_level
if df["severity_score"].nunique() >= 3:
    df["severity_rank"] = df["severity_score"].rank(method="first")
    df["severity_level"] = pd.qcut(
        df["severity_rank"],
        q=3,
        labels=["Low", "Medium", "High"]
    )
else:
    df["severity_level"] = "Low"

# Final clean dataset
climate_clean = pd.DataFrame({
    "event_id": df["DisNo."],
    "event_type": df["Disaster Type"],
    "event_date": df["event_date"],
    "location": df["Location"],
    "severity_level": df["severity_level"],
    "severity_score": df["severity_score"]
})

# Drop invalid rows
climate_clean = climate_clean.dropna(subset = ["event_date"])

# Sort
climate_clean = climate_clean.sort_values("event_date").reset_index(drop = True)

# Save
climate_clean.to_csv(OUTPUT_FILE, index = False)

print("\n✅ Final dataset created")
print("Shape:", climate_clean.shape)
print("\nColumns:", climate_clean.columns.tolist())
print("\nSample:")
print(climate_clean.head())