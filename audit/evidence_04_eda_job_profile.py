from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "processed" / "cleaned_postings.csv"

df = pd.read_csv(DATASET)

print("=" * 85)
print("EXPLORATORY DATA ANALYSIS – JOB POSTING PROFILE")
print("=" * 85)

print("\n" + "=" * 85)
print("1. DATASET OVERVIEW")
print("=" * 85)

print(f"\nJob Postings           : {len(df):,}")
print(f"Variables              : {len(df.columns)}")

# ---------------------------------------------------------
# Job titles
# ---------------------------------------------------------

if "title" in df.columns:

    print("\n" + "=" * 85)
    print("2. MOST FREQUENT JOB TITLES")
    print("=" * 85)

    titles = (
        df["title"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .head(15)
    )

    print("\n" + titles.to_string())

# ---------------------------------------------------------
# Work type
# ---------------------------------------------------------

work_columns = [
    "formatted_work_type",
    "work_type"
]

work_col = next(
    (c for c in work_columns if c in df.columns),
    None
)

if work_col:

    print("\n" + "=" * 85)
    print("3. WORK TYPE DISTRIBUTION")
    print("=" * 85)

    work = (
        df[work_col]
        .dropna()
        .astype(str)
        .value_counts()
    )

    result = pd.DataFrame({
        "Postings": work,
        "Percentage": (work / len(df) * 100).round(2)
    })

    print("\n" + result.to_string())

# ---------------------------------------------------------
# Experience
# ---------------------------------------------------------

experience_columns = [
    "formatted_experience_level",
    "experience_level"
]

experience_col = next(
    (c for c in experience_columns if c in df.columns),
    None
)

if experience_col:

    print("\n" + "=" * 85)
    print("4. EXPERIENCE LEVEL DISTRIBUTION")
    print("=" * 85)

    experience = (
        df[experience_col]
        .dropna()
        .astype(str)
        .value_counts()
    )

    result = pd.DataFrame({
        "Postings": experience,
        "Percentage": (experience / len(df) * 100).round(2)
    })

    print("\n" + result.to_string())

# ---------------------------------------------------------
# Location
# ---------------------------------------------------------

if "location" in df.columns:

    print("\n" + "=" * 85)
    print("5. TOP JOB LOCATIONS")
    print("=" * 85)

    locations = (
        df["location"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .head(15)
    )

    print("\n" + locations.to_string())

print("\n" + "=" * 85)
print("EDA SUMMARY")
print("=" * 85)

print(
    "\nThe cleaned dataset was examined across job titles, "
    "work types, experience levels and locations to understand "
    "the structure and distribution of the job-posting data."
)

print("\nStatus : INITIAL EDA COMPLETED")
print("=" * 85)