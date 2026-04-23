import pandas as pd
import numpy as np
from pathlib import Path

# Paths
EVENT_FILE = "data/processed/event_study_results.csv"
OUTPUT_FILE = "data/processed/stress_test_results.csv"

Path("data/processed").mkdir(parents=True, exist_ok=True)

# Load event study data
df = pd.read_csv(EVENT_FILE)

print("Loaded event study data:", df.shape)

# Basic stats from historical data
mean_impact = df["impact"].mean()
std_impact = df["impact"].std()

print("Mean impact:", mean_impact)
print("Std impact:", std_impact)

# simulation parameters
N_SIMULATIONS = 1000
EVENT_PER_YEAR = 10   # assumed number of climate events

# Monte Carlo simulation
simulated_losses = []

for i in range(N_SIMULATIONS):
    yearly_impact = np.random.normal(
        loc = mean_impact,
        scale = std_impact,
        size = EVENT_PER_YEAR
    )

    total_impact = yearly_impact.sum()

    simulated_losses.append(total_impact)

# Convert to DataFrame
sim_df = pd.DataFrame({
    "simulation": range(N_SIMULATIONS),
    "total_impact": simulated_losses
})

# Risk Metrics
var_95 = np.percentile(sim_df["total_impact"], 5)
var_99 = np.percentile(sim_df["total_impact"], 1)

avg_loss = sim_df["total_impact"].mean()

summary = pd.DataFrame({
    "metric": ["Average Impact", "VaR 95%", "VaR 99%"],
    "value": [avg_loss, var_95, var_99]
})

# Savae results
sim_df.to_csv(OUTPUT_FILE, index = False)
summary.to_csv("data/processed/stress_summary.csv", index = False)

print("\n Stress testing completed")
print("Saved to:", OUTPUT_FILE)
print("\nSummary:")
print(summary)