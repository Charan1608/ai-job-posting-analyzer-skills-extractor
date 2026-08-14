"""
==============================================================
Dataset Profiler
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Version : 1.0
==============================================================
"""

from pathlib import Path
import pandas as pd


def get_project_root():
    """Return project root folder."""
    return Path(__file__).resolve().parents[2]


def profile_dataset(csv_file):
    """
    Profile one dataset and return
    column level statistics.
    """

    df = pd.read_csv(csv_file)

    profile = []

    total_rows = len(df)

    for column in df.columns:

        missing = df[column].isnull().sum()

        missing_percent = round((missing / total_rows) * 100, 2)

        profile.append({

            "Dataset": csv_file.name,

            "Column": column,

            "Data Type": str(df[column].dtype),

            "Rows": total_rows,

            "Unique Values": df[column].nunique(),

            "Missing Values": missing,

            "Missing %": missing_percent

        })

    return pd.DataFrame(profile)


def main():

    print("=" * 70)
    print("DATASET PROFILER")
    print("=" * 70)

    project_root = get_project_root()

    raw_folder = project_root / "data" / "raw"

    output_folder = project_root / "reports" / "profiling"

    output_folder.mkdir(parents=True, exist_ok=True)

    csv_files = list(raw_folder.rglob("*.csv"))

    all_profiles = []

    print(f"\nFound {len(csv_files)} CSV files.\n")

    for file in csv_files:

        print(f"Profiling {file.name}")

        profile = profile_dataset(file)

        all_profiles.append(profile)

    final_profile = pd.concat(all_profiles, ignore_index=True)

    output_file = output_folder / "column_profile.csv"

    final_profile.to_csv(output_file, index=False)

    print("\nCompleted Successfully")

    print(f"\nReport Saved : {output_file}")


if __name__ == "__main__":
    main()