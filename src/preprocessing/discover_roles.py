import pandas as pd
import re
from pathlib import Path

print("=" * 70)
print("ROLE DISCOVERY")
print("=" * 70)

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

data_path = Path("data/interim/business_analytics_postings.csv")
taxonomy_path = Path("taxonomy/role_taxonomy.csv")
report_folder = Path("reports/filtering")

report_folder.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = pd.read_csv(data_path)
taxonomy = pd.read_csv(taxonomy_path)

taxonomy["Include"] = taxonomy["Include"].astype(bool)
taxonomy = taxonomy[taxonomy["Include"] == True]

# ---------------------------------------------------
# Role Classifier
# ---------------------------------------------------

def classify_role(title):

    title = str(title).lower()

    for _, row in taxonomy.iterrows():

        pattern = str(row["Regex_Pattern"]).lower()

        if re.search(pattern, title):
            return row["Role_Family"]

    return "Other"

# ---------------------------------------------------
# Classify
# ---------------------------------------------------

df["Role"] = df["title"].apply(classify_role)

# ---------------------------------------------------
# Unknown Roles
# ---------------------------------------------------

unknown = df[df["Role"] == "Other"]

unknown_titles = (
    unknown["title"]
    .value_counts()
    .reset_index()
)

unknown_titles.columns = ["Job Title", "Count"]

print()
print("Unknown Roles Found :", len(unknown_titles))
print()

print(unknown_titles.head(30))

# ---------------------------------------------------
# Save Report
# ---------------------------------------------------

output_file = report_folder / "unknown_roles.csv"

unknown_titles.to_csv(output_file, index=False)

print()
print("Report Saved Successfully")
print(output_file)