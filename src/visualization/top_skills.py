"""
=========================================================
TOP SKILLS ANALYSIS
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("TOP SKILLS ANALYSIS")
print("=" * 70)

# ----------------------------------------------------
# Project Root
# ----------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# ----------------------------------------------------
# Files
# ----------------------------------------------------

ba_jobs_file = ROOT / "data" / "interim" / "business_analytics_postings.csv"

job_skills_file = (
    ROOT
    / "data"
    / "raw"
    / "jobs"
    / "job_skills.csv"
)

skills_file = (
    ROOT
    / "data"
    / "raw"
    / "mappings"
    / "skills.csv"
)

report_folder = ROOT / "reports" / "eda"
report_folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# Load
# ----------------------------------------------------

ba_jobs = pd.read_csv(ba_jobs_file)

job_skills = pd.read_csv(job_skills_file)

skills = pd.read_csv(skills_file)

# ----------------------------------------------------
# Keep only Business Analytics jobs
# ----------------------------------------------------

job_skills = job_skills[
    job_skills["job_id"].isin(
        ba_jobs["job_id"]
    )
]

# ----------------------------------------------------
# Merge
# ----------------------------------------------------

merged = job_skills.merge(
    skills,
    on="skill_abr",
    how="left"
)

# ----------------------------------------------------
# Count
# ----------------------------------------------------

summary = (
    merged["skill_name"]
    .fillna("Unknown Skill")
    .value_counts()
    .head(20)
    .reset_index()
)

summary.columns = ["Skill", "Count"]

print(summary)

# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

summary.to_csv(
    report_folder / "top_skills.csv",
    index=False
)

# ----------------------------------------------------
# Plot
# ----------------------------------------------------

plt.figure(figsize=(12,8))

plt.barh(
    summary["Skill"],
    summary["Count"]
)

plt.gca().invert_yaxis()

plt.title(
    "Top Skills Required for Business Analytics Jobs"
)

plt.xlabel("Number of Job Postings")

plt.tight_layout()

plt.savefig(
    report_folder / "top_skills.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "top_skills.csv")
print(report_folder / "top_skills.png")