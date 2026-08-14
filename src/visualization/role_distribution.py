import pandas as pd
import matplotlib.pyplot as plt
import re
from pathlib import Path

# =====================================================
# ROLE DISTRIBUTION
# =====================================================

print("=" * 70)
print("ROLE DISTRIBUTION")
print("=" * 70)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

data_path = Path("data/interim/business_analytics_postings.csv")
taxonomy_path = Path("taxonomy/role_taxonomy.csv")
report_folder = Path("reports/eda")

report_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)
taxonomy = pd.read_csv(taxonomy_path)

# -----------------------------------------------------
# Keep only Included Roles
# -----------------------------------------------------

taxonomy["Include"] = taxonomy["Include"].astype(bool)
taxonomy = taxonomy[taxonomy["Include"] == True]

# -----------------------------------------------------
# Role Matching Function
# -----------------------------------------------------

def classify_role(job_title):

    title = str(job_title).lower()

    for _, row in taxonomy.iterrows():

        pattern = str(row["Regex_Pattern"]).lower()

        if re.search(pattern, title):
            return row["Role_Family"]

    return "Other"

# -----------------------------------------------------
# Apply Classification
# -----------------------------------------------------

df["Role"] = df["title"].apply(classify_role)

summary = (
    df["Role"]
    .value_counts()
    .reset_index()
)

summary.columns = ["Role", "Count"]

print()
print(summary)

# -----------------------------------------------------
# Save CSV
# -----------------------------------------------------

summary.to_csv(
    report_folder / "role_distribution.csv",
    index=False
)

# -----------------------------------------------------
# Plot
# -----------------------------------------------------

plt.figure(figsize=(12,6))

plt.bar(summary["Role"], summary["Count"])

plt.title("Business Analytics Role Distribution")

plt.ylabel("Number of Job Postings")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    report_folder / "role_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")
print(report_folder / "role_distribution.csv")
print(report_folder / "role_distribution.png")