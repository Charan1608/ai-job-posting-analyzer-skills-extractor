from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = ROOT / "data" / "raw" / "postings.csv"
CLEAN_FILE = ROOT / "data" / "processed" / "cleaned_postings.csv"

raw = pd.read_csv(RAW_FILE)
clean = pd.read_csv(CLEAN_FILE)

print("=" * 85)
print("DATA CLEANING AND PREPROCESSING SUMMARY")
print("=" * 85)

print("\n" + "=" * 85)
print("1. DATASET SIZE BEFORE AND AFTER CLEANING")
print("=" * 85)

print(f"\nRaw Dataset Records       : {len(raw):,}")
print(f"Cleaned Dataset Records   : {len(clean):,}")

removed = len(raw) - len(clean)

print(f"Records Removed           : {removed:,}")

if len(raw) > 0:
    retention = len(clean) / len(raw) * 100
    print(f"Data Retention            : {retention:.2f}%")

print("\n" + "=" * 85)
print("2. STRUCTURAL COMPARISON")
print("=" * 85)

print(f"\nRaw Dataset Shape         : {raw.shape}")
print(f"Cleaned Dataset Shape     : {clean.shape}")

print(f"Raw Columns               : {len(raw.columns)}")
print(f"Cleaned Columns           : {len(clean.columns)}")

print("\n" + "=" * 85)
print("3. CLEANED DATA COMPLETENESS")
print("=" * 85)

missing = clean.isna().sum()
missing_pct = (missing / len(clean) * 100).round(2)

quality = pd.DataFrame({
    "Missing Values": missing,
    "Missing %": missing_pct
})

quality = quality[quality["Missing Values"] > 0] \
    .sort_values("Missing %", ascending=False)

if len(quality) == 0:
    print("\nNo missing values detected in the cleaned dataset.")
else:
    print("\nRemaining Missing-Value Fields:")
    print(
        quality.head(10).to_string(
            formatters={"Missing %": "{:.2f}%".format}
        )
    )

print("\n" + "=" * 85)
print("4. CORE FIELD AVAILABILITY")
print("=" * 85)

core_fields = [
    "job_id",
    "company_name",
    "title",
    "description",
    "location"
]

for col in core_fields:
    if col in clean.columns:
        completeness = clean[col].notna().mean() * 100
        print(f"{col:<25} : {completeness:>7.2f}% complete")

print("\n" + "=" * 85)
print("5. CLEANED DATA SAMPLE")
print("=" * 85)

sample_columns = [
    "job_id",
    "company_name",
    "title",
    "location"
]

sample_columns = [
    c for c in sample_columns
    if c in clean.columns
]

print(
    clean[sample_columns]
    .head(8)
    .to_string(index=False)
)

print("\n" + "=" * 85)
print("PREPROCESSING STATUS")
print("=" * 85)

print("\nRaw job postings successfully transformed into")
print("a structured analytical dataset for subsequent")
print("skill extraction, normalization and machine learning.")

print("\nStatus : CLEANED DATASET READY")
print("=" * 85)