from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("TOP COMPANIES ANALYSIS")
print("=" * 70)

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

postings_file = Path("data/interim/business_analytics_postings.csv")
companies_file = Path("data/raw/companies/companies.csv")
report_folder = Path("reports/eda")

report_folder.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# Load data
# ---------------------------------------------------

postings = pd.read_csv(postings_file)
companies = pd.read_csv(companies_file)

# ---------------------------------------------------
# Join company names
# ---------------------------------------------------

merged = postings.merge(
    companies[["company_id", "name"]],
    on="company_id",
    how="left"
)

merged["name"] = merged["name"].fillna("Unknown Company")

summary = (
    merged["name"]
    .value_counts()
    .head(20)
    .reset_index()
)

summary.columns = ["Company", "Job Postings"]

print(summary)

# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

summary.to_csv(
    report_folder / "company_distribution.csv",
    index=False
)

# ---------------------------------------------------
# Plot
# ---------------------------------------------------

plt.figure(figsize=(12,8))

plt.barh(
    summary["Company"][::-1],
    summary["Job Postings"][::-1]
)

plt.title("Top Companies Hiring Business Analytics Professionals")

plt.xlabel("Number of Job Postings")

plt.tight_layout()

plt.savefig(
    report_folder / "company_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "company_distribution.csv")
print(report_folder / "company_distribution.png")