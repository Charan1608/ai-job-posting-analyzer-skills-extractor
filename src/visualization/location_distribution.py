from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("LOCATION DISTRIBUTION")
print("=" * 70)

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

input_file = Path("data/interim/business_analytics_postings.csv")
report_folder = Path("reports/eda")

report_folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Load
# ----------------------------------------------------

df = pd.read_csv(input_file)

# ----------------------------------------------------
# Clean Location
# ----------------------------------------------------

df["location"] = (
    df["location"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)

summary = (
    df["location"]
    .value_counts()
    .head(20)
    .reset_index()
)

summary.columns = ["Location", "Job Postings"]

print(summary)

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

summary.to_csv(
    report_folder / "location_distribution.csv",
    index=False
)

# ----------------------------------------------------
# Plot
# ----------------------------------------------------

plt.figure(figsize=(12,8))

plt.barh(
    summary["Location"][::-1],
    summary["Job Postings"][::-1]
)

plt.title("Top Hiring Locations")

plt.xlabel("Number of Job Postings")

plt.tight_layout()

plt.savefig(
    report_folder / "location_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "location_distribution.csv")
print(report_folder / "location_distribution.png")