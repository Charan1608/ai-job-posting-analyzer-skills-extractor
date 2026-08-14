"""
=========================================================
INDUSTRY DISTRIBUTION
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("INDUSTRY DISTRIBUTION")
print("=" * 70)

# ----------------------------------------------------
# Project Root
# ----------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# ----------------------------------------------------
# Input Files
# ----------------------------------------------------

postings_file = ROOT / "data" / "interim" / "business_analytics_postings.csv"

job_industries_file = (
    ROOT
    / "data"
    / "raw"
    / "jobs"
    / "job_industries.csv"
)

industries_file = (
    ROOT
    / "data"
    / "raw"
    / "mappings"
    / "industries.csv"
)

report_folder = ROOT / "reports" / "eda"
report_folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

postings = pd.read_csv(postings_file)

job_industries = pd.read_csv(job_industries_file)

industries = pd.read_csv(industries_file)

print(f"Business Analytics Jobs : {len(postings):,}")
print(f"Job-Industry Records    : {len(job_industries):,}")
print(f"Industries             : {len(industries):,}")

# ----------------------------------------------------
# Merge
# ----------------------------------------------------

merged = postings.merge(
    job_industries,
    on="job_id",
    how="left"
)

merged = merged.merge(
    industries,
    on="industry_id",
    how="left"
)

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

summary = (
    merged["industry_name"]
    .fillna("Unknown")
    .value_counts()
    .head(20)
    .reset_index()
)

summary.columns = ["Industry", "Job Postings"]

print("\nTop Industries\n")
print(summary)

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

summary.to_csv(
    report_folder / "industry_distribution.csv",
    index=False
)

# ----------------------------------------------------
# Plot
# ----------------------------------------------------

plt.figure(figsize=(12,8))

plt.barh(
    summary["Industry"],
    summary["Job Postings"]
)

plt.gca().invert_yaxis()

plt.title(
    "Top Industries Hiring Business Analytics Professionals"
)

plt.xlabel("Number of Job Postings")

plt.tight_layout()

plt.savefig(
    report_folder / "industry_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "industry_distribution.csv")
print(report_folder / "industry_distribution.png")