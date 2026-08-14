import pandas as pd

SOURCE = "data/labelled/gold_standard_200.csv"
EXTRACTED = "data/processed/sample_200_with_ai_skills.csv"

# -----------------------------
# Load files
# -----------------------------

source = pd.read_csv(SOURCE)
extracted = pd.read_csv(EXTRACTED)

# -----------------------------
# Merge extraction columns
# -----------------------------

cols = [
    "job_id",
    "technical_skills",
    "soft_skills",
    "tools",
    "certifications",
    "experience",
    "education",
]

merged = source.merge(

    extracted[cols],

    on="job_id",

    how="left",

    suffixes=("", "_old")

)

# -----------------------------
# Fill empty extraction fields
# -----------------------------

for col in [
    "technical_skills",
    "soft_skills",
    "tools",
    "certifications",
]:

    merged[col] = merged[col].fillna("[]")

merged["experience"] = merged["experience"].fillna("")
merged["education"] = merged["education"].fillna("")

# -----------------------------
# Save
# -----------------------------

merged.to_csv(

    EXTRACTED,

    index=False

)

print("=" * 60)
print("EXTRACTION FILE REBUILT")
print("=" * 60)
print("Rows :", len(merged))

print(
    "Completed :",
    (
        merged["technical_skills"] != "[]"
    ).sum()
)

print(
    "Pending :",
    (
        merged["technical_skills"] == "[]"
    ).sum()
)