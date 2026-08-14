"""
==============================================================
Dataset Cleaner
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Version : 1.0
==============================================================
"""

from pathlib import Path
import pandas as pd
import re


def clean_text(text):
    """Clean text for NLP."""

    if pd.isna(text):
        return ""

    text = str(text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\\S+|www\\.\\S+", " ", text)

    # Replace line breaks and tabs
    text = text.replace("\\n", " ")
    text = text.replace("\\r", " ")
    text = text.replace("\\t", " ")

    # Remove extra spaces
    text = re.sub(r"\\s+", " ", text)

    return text.strip()


def main():

    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "interim"
        / "business_analytics_postings.csv"
    )

    output_folder = (
        project_root
        / "data"
        / "processed"
    )

    report_folder = (
        project_root
        / "reports"
        / "preprocessing"
    )

    output_folder.mkdir(parents=True, exist_ok=True)
    report_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("DATASET CLEANER")
    print("=" * 70)

    df = pd.read_csv(input_file)

    original_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    duplicates_removed = original_rows - len(df)

    # Remove missing descriptions
    before = len(df)

    df = df[df["description"].notna()]

    missing_removed = before - len(df)

    # Clean descriptions
    df["clean_description"] = df["description"].apply(clean_text)

    output_file = output_folder / "cleaned_postings.csv"

    df.to_csv(output_file, index=False)

    report = pd.DataFrame({
        "Metric": [
            "Original Records",
            "Duplicates Removed",
            "Missing Descriptions Removed",
            "Final Records"
        ],
        "Value": [
            original_rows,
            duplicates_removed,
            missing_removed,
            len(df)
        ]
    })

    report.to_csv(
        report_folder / "cleaning_report.csv",
        index=False
    )

    print(f"Original Records : {original_rows:,}")
    print(f"Duplicates Removed : {duplicates_removed:,}")
    print(f"Missing Descriptions Removed : {missing_removed:,}")
    print(f"Final Records : {len(df):,}")

    print("\nCleaning Completed Successfully")


if __name__ == "__main__":
    main()