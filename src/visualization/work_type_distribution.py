from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("WORK TYPE DISTRIBUTION")
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
# Select work type column
# ----------------------------------------------------

column = None

for col in [
    "formatted_work_type",
    "work_type",
    "formatted_worktype"
]:
    if col in df.columns:
        column = col
        break

if column is None:
    print("No Work Type column found.")
    exit()

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

summary = (
    df[column]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .value_counts()
    .reset_index()
)

summary.columns = ["Work Type", "Job Postings"]

print(summary)

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

summary.to_csv(
    report_folder / "work_type_distribution.csv",
    index=False
)

# ----------------------------------------------------
# Plot
# ----------------------------------------------------

plt.figure(figsize=(9,6))

plt.bar(
    summary["Work Type"],
    summary["Job Postings"]
)

plt.title("Work Type Distribution")

plt.xlabel("Work Type")

plt.ylabel("Number of Job Postings")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    report_folder / "work_type_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "work_type_distribution.csv")
print(report_folder / "work_type_distribution.png")