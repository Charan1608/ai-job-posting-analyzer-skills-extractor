import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 4.0 RAW DATASET EDA
# AI-Powered Job Posting Analyzer & Skills Extractor
# ============================================================

print("\n" + "=" * 70)
print("4.0 RAW DATASET – EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# ------------------------------------------------------------
# 1. Locate raw dataset
# ------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "postings.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "audit",
    "evidence",
    "outputs",
    "04_raw_eda"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


print("\nProject root:")
print(PROJECT_ROOT)

print("\nRaw dataset:")
print(DATA_FILE)


if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(
        f"\nRaw dataset not found:\n{DATA_FILE}"
    )


# ------------------------------------------------------------
# 2. Load raw dataset
# ------------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("\n" + "-" * 70)
print("RAW DATASET LOADED")
print("-" * 70)

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}")


# ------------------------------------------------------------
# 3. Dataset structure
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("DATASET STRUCTURE")
print("-" * 70)

print("\nColumn names:")

for i, col in enumerate(df.columns, start=1):
    print(f"{i:02d}. {col}")


# ------------------------------------------------------------
# 4. Missing-value analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("MISSING VALUE ANALYSIS")
print("-" * 70)

missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100

missing_table = pd.DataFrame({
    "missing_count": missing,
    "missing_percentage": missing_pct.round(2)
})

missing_table = missing_table[
    missing_table["missing_count"] > 0
].sort_values(
    "missing_count",
    ascending=False
)

print(missing_table.to_string())


# Save missing-value summary
missing_table.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "raw_missing_values.csv"
    )
)


# ------------------------------------------------------------
# 5. Duplicate analysis
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("DUPLICATE ANALYSIS")
print("-" * 70)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count:,}")


# ------------------------------------------------------------
# 6. Job title distribution
# ------------------------------------------------------------

if "title" in df.columns:

    print("\n" + "-" * 70)
    print("TOP JOB TITLES")
    print("-" * 70)

    title_counts = (
        df["title"]
        .dropna()
        .astype(str)
        .value_counts()
        .head(15)
    )

    print(title_counts.to_string())


    plt.figure(figsize=(10, 6))

    title_counts.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Top 15 Job Titles in Raw Dataset"
    )

    plt.xlabel("Number of Job Postings")
    plt.ylabel("Job Title")

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "01_raw_job_title_distribution.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"\nSaved: {output}")


# ------------------------------------------------------------
# 7. Employment type distribution
# ------------------------------------------------------------

if "formatted_work_type" in df.columns:

    print("\n" + "-" * 70)
    print("EMPLOYMENT TYPE DISTRIBUTION")
    print("-" * 70)

    work_type_counts = (
        df["formatted_work_type"]
        .dropna()
        .astype(str)
        .value_counts()
    )

    print(work_type_counts.to_string())


    plt.figure(figsize=(9, 6))

    work_type_counts.plot(
        kind="bar"
    )

    plt.title(
        "Employment Type Distribution – Raw Dataset"
    )

    plt.xlabel("Employment Type")
    plt.ylabel("Number of Job Postings")

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "02_raw_employment_type.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"\nSaved: {output}")


# ------------------------------------------------------------
# 8. Experience level distribution
# ------------------------------------------------------------

if "formatted_experience_level" in df.columns:

    print("\n" + "-" * 70)
    print("EXPERIENCE LEVEL DISTRIBUTION")
    print("-" * 70)

    experience_counts = (
        df["formatted_experience_level"]
        .dropna()
        .astype(str)
        .value_counts()
    )

    print(experience_counts.to_string())


    plt.figure(figsize=(9, 6))

    experience_counts.plot(
        kind="bar"
    )

    plt.title(
        "Experience Level Distribution – Raw Dataset"
    )

    plt.xlabel("Experience Level")
    plt.ylabel("Number of Job Postings")

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "03_raw_experience_level.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"\nSaved: {output}")


# ------------------------------------------------------------
# 9. Remote vs On-site
# ------------------------------------------------------------

if "remote_allowed" in df.columns:

    print("\n" + "-" * 70)
    print("REMOTE WORK ANALYSIS")
    print("-" * 70)

    remote_counts = (
        df["remote_allowed"]
        .fillna(False)
        .astype(bool)
        .map({
            True: "Remote",
            False: "Non-Remote"
        })
        .value_counts()
    )

    print(remote_counts.to_string())


    plt.figure(figsize=(8, 6))

    remote_counts.plot(
        kind="bar"
    )

    plt.title(
        "Remote vs Non-Remote Jobs – Raw Dataset"
    )

    plt.xlabel("Work Arrangement")
    plt.ylabel("Number of Job Postings")

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "04_raw_remote_vs_nonremote.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"\nSaved: {output}")


# ------------------------------------------------------------
# 10. Location analysis
# ------------------------------------------------------------

if "location" in df.columns:

    print("\n" + "-" * 70)
    print("TOP JOB LOCATIONS")
    print("-" * 70)

    location_counts = (
        df["location"]
        .dropna()
        .astype(str)
        .value_counts()
        .head(15)
    )

    print(location_counts.to_string())


    plt.figure(figsize=(10, 6))

    location_counts.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Top 15 Job Locations – Raw Dataset"
    )

    plt.xlabel("Number of Job Postings")
    plt.ylabel("Location")

    plt.tight_layout()

    output = os.path.join(
        OUTPUT_DIR,
        "05_raw_location_distribution.png"
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"\nSaved: {output}")


# ------------------------------------------------------------
# 11. Final summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RAW DATASET EDA COMPLETED")
print("=" * 70)

print(f"\nRaw dataset records : {len(df):,}")
print(f"Raw dataset columns : {len(df.columns):,}")

print("\nGenerated outputs:")

for filename in sorted(os.listdir(OUTPUT_DIR)):
    print(f" - {filename}")

print("\nRaw EDA evidence saved successfully.")
print("=" * 70)