import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Path
EVENT_FILE = "data/processed/event_study_results.csv"
SECTOR_FILE = "data/processed/sector_event_impact.csv"
STRESS_FILE = "data/processed/stress_test_results.csv"

OUTPUT_DIR = Path("data/processed/visuals")
OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

# Load data
events = pd.read_csv(EVENT_FILE)
sector = pd.read_csv(SECTOR_FILE)

events["impact"] = pd.to_numeric(events["impact"], errors = "coerce")
sector["avg_impact"] = pd.to_numeric(sector["avg_impact"], errors = "coerce")

events = events.dropna(subset = ["impact"])
sector = sector.dropna(subset = ["avg_impact"])

# 1. Sector Impact
sector_plot = (
    sector.groupby("sector", as_index = False)["avg_impact"]
    .mean()
    .sort_values("avg_impact")
)

plt.figure(figsize = (10,6))
plt.bar(sector_plot["sector"], sector_plot["avg_impact"])
plt.title("Average Climate Event Impact by Sector")
plt.xlabel("Sector")
plt.ylabel("Average Impact")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sector_impact.png")
plt.close()

# 2. Event type impact chart
event_type_plot = (
    events.groupby("event_type", as_index = False)["impact"]
    .mean()
    .sort_values("impact")
)

plt.figure(figsize = (10,6))
plt.bar(event_type_plot["event_type"], event_type_plot["impact"])
plt.title("Average Market Impact by Climate Event Type ")
plt.xlabel("Event Type")
plt.ylabel("Average Impact")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "event_type_impact.png")
plt.close()

# 3. Impact Distribution
plt.figure(figsize = (10,6))
plt.hist(events["impact"], bins = 30)
plt.title("Distribution of Climate Event Impact")
plt.xlabel("Impact")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "impact_distribution.png")
plt.close()

# 4. Sector vs event type heatmap
heatmap_data = events.pivot_table(
    index = "sector",
    columns = "event_type",
    values = "impact",
    aggfunc = "mean"
)

plt.figure(figsize = (10,6))
sns.heatmap(heatmap_data, annot = True, fmt = ".3f", cmap = "coolwarm", linewidths = 0.5, linecolor = "gray", cbar_kws = {"label": "Average Impact"})
plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns, rotation = 45)
plt.yticks(range(len(heatmap_data.index)),heatmap_data.index)
plt.title("Sector Sensitivity by Climate Event Type")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sector_event_heatmap.png")
plt.close()

# 5. Stress Test Distribution
if Path(STRESS_FILE).exists():
    stress = pd.read_csv(STRESS_FILE)

    if "total_impact" in stress.columns:
        stress["total_imipact"] = pd.to_numeric(stress["total_impact"], errors = "coerce")
        stress = stress.dropna(subset = ["total_impact"])

        plt.figure(figsize = (10,6))
        plt.hist(stress["total_impact"], bins = 30)
        plt.title("Monte Carlo Stress Test Impact Distribution")
        plt.xlabel("Simulated total Impact")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "stress_test_distribution.png")
        plt.close()

print("Charts created successfully")
print(f"Saved in: {OUTPUT_DIR}")