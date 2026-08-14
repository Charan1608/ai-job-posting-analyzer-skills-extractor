from pathlib import Path
import pandas as pd


# ============================================================
# RAW DATASET EVIDENCE
# AI-POWERED JOB POSTING ANALYZER & SKILLS EXTRACTOR
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "data" / "raw" / "postings.csv"


def print_section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


print("=" * 78)
print("RAW DATASET ACQUISITION AND INITIAL DATA OVERVIEW")
print("=" * 78)

print("\nProject      : AI-Powered Job Posting Analyzer & Skills Extractor")
print("Dataset      : LinkedIn Job Postings Dataset (2023–2024)")
print("Source       : Kaggle")
print(f"Local File   : {DATASET}")

if not DATASET.exists():
    raise FileNotFoundError(
        f"\nRaw dataset not found:\n{DATASET}"
    )


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(DATASET, low_memory=False)


# ------------------------------------------------------------
# DATASET DIMENSIONS
# ------------------------------------------------------------

print_section("1. DATASET DIMENSIONS")

print(f"Total Records      : {len(df):,}")
print(f"Total Variables    : {len(df.columns):,}")
print(f"Dataset Shape      : {df.shape}")


# ------------------------------------------------------------
# COLUMN INVENTORY
# ------------------------------------------------------------

print_section("2. COLUMN INVENTORY")

for number, column in enumerate(df.columns, start=1):
    print(f"{number:02d}. {column}")


# ------------------------------------------------------------
# DATA TYPES
# ------------------------------------------------------------

print_section("3. DATA TYPE PROFILE")

dtype_summary = df.dtypes.value_counts()

for dtype, count in dtype_summary.items():
    print(f"{str(dtype):<15} : {count} columns")


# ------------------------------------------------------------
# MISSING VALUE OVERVIEW
# ------------------------------------------------------------

print_section("4. MISSING VALUE OVERVIEW")

missing = df.isna().sum()
missing_pct = (missing / len(df)) * 100

missing_table = pd.DataFrame({
    "Missing Values": missing,
    "Missing %": missing_pct.round(2)
})

missing_table = missing_table[
    missing_table["Missing Values"] > 0
].sort_values(
    "Missing Values",
    ascending=False
)

print(f"Columns with Missing Values : {len(missing_table)}")

if len(missing_table) > 0:
    print("\nTop Missing-Value Columns:")
    print(missing_table.head(20).to_string())
else:
    print("No missing values detected.")


# ------------------------------------------------------------
# SAMPLE RECORDS
# ------------------------------------------------------------

print_section("5. SAMPLE RECORDS")

# Display selected fields so the evidence remains readable.
preferred_columns = [
    "job_id",
    "company_name",
    "title",
    "location",
    "formatted_work_type",
    "formatted_experience_level",
    "remote_allowed",
]

available_columns = [
    column for column in preferred_columns
    if column in df.columns
]

print(
    df[available_columns]
    .head(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# KEY FIELD AVAILABILITY
# ------------------------------------------------------------

print_section("6. KEY JOB-POSTING FIELDS")

key_fields = [
    "job_id",
    "company_name",
    "title",
    "description",
    "location",
    "formatted_work_type",
    "formatted_experience_level",
    "skills_desc",
    "remote_allowed",
    "max_salary",
    "min_salary",
]

for field in key_fields:
    if field in df.columns:
        non_null = df[field].notna().sum()
        completeness = (non_null / len(df)) * 100

        print(
            f"{field:<30} "
            f"Available: Yes   "
            f"Non-null: {non_null:,}   "
            f"Completeness: {completeness:.2f}%"
        )
    else:
        print(
            f"{field:<30} "
            f"Available: No"
        )


# ------------------------------------------------------------
# UNIQUE VALUES IN IMPORTANT FIELDS
# ------------------------------------------------------------

print_section("7. UNIQUE VALUE PROFILE")

for field in [
    "job_id",
    "company_name",
    "title",
    "location",
    "formatted_work_type",
    "formatted_experience_level",
]:
    if field in df.columns:
        print(
            f"{field:<30} : "
            f"{df[field].nunique(dropna=True):,} unique values"
        )


# ------------------------------------------------------------
# TOP JOB TITLES
# ------------------------------------------------------------

if "title" in df.columns:

    print_section("8. MOST FREQUENT JOB TITLES")

    title_counts = (
        df["title"]
        .astype(str)
        .value_counts()
        .head(15)
    )

    print(title_counts.to_string())


# ------------------------------------------------------------
# FINAL DATASET STATUS
# ------------------------------------------------------------

print_section("9. INITIAL DATASET STATUS")

print("Status : RAW DATASET SUCCESSFULLY LOADED")
print(f"Records : {len(df):,}")
print(f"Variables : {len(df.columns):,}")

print("\nThe raw dataset is ready for the subsequent")
print("data profiling, cleaning, normalization, feature")
print("engineering, machine-learning and analytical stages.")

print("\n" + "=" * 78)
print("RAW DATASET EVIDENCE COMPLETE")
print("=" * 78)