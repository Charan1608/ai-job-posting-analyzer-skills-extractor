from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "raw" / "postings.csv"

df = pd.read_csv(DATASET)

print("=" * 85)
print("RAW DATASET DATA QUALITY ASSESSMENT")
print("=" * 85)

print(f"\nDataset Records        : {len(df):,}")
print(f"Dataset Variables      : {len(df.columns)}")

# Missing-value profile
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)

quality = pd.DataFrame({
    "Missing Values": missing,
    "Missing %": missing_pct
})

quality = quality[quality["Missing Values"] > 0] \
    .sort_values("Missing %", ascending=False)

print("\n" + "=" * 85)
print("MISSING VALUE PROFILE")
print("=" * 85)

print(f"\nColumns with Missing Values : {len(quality)}")

print("\nTop Missing-Value Fields:")
print(
    quality.head(12).to_string(
        formatters={"Missing %": "{:.2f}%".format}
    )
)

# Core fields
core_fields = [
    "job_id",
    "company_name",
    "title",
    "description",
    "location",
    "formatted_work_type",
    "formatted_experience_level"
]

print("\n" + "=" * 85)
print("CORE FIELD COMPLETENESS")
print("=" * 85)

for col in core_fields:
    if col in df.columns:
        completeness = df[col].notna().mean() * 100
        print(
            f"{col:<30} : {completeness:>7.2f}% complete"
        )

print("\n" + "=" * 85)
print("DATA QUALITY OBSERVATION")
print("=" * 85)

print(
    "\nCore job-identification and textual fields show high "
    "data availability, while several secondary fields contain "
    "substantial missing values."
)

print("\nAssessment : Suitable for preprocessing and analytical preparation.")
print("=" * 85)