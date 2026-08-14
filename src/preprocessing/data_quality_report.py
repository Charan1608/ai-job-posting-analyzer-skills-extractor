"""
==============================================================
Data Quality Assessment
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Version : 1.0
==============================================================
"""

from pathlib import Path
import pandas as pd
import re


def main():

    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "processed"
        / "cleaned_postings.csv"
    )

    report_folder = (
        project_root
        / "reports"
        / "preprocessing"
    )

    report_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 70)

    df = pd.read_csv(input_file)

    total_rows = len(df)

    duplicate_job_ids = df["job_id"].duplicated().sum()

    empty_descriptions = (
        df["clean_description"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    short_descriptions = (
        df["clean_description"]
        .str.len()
        .lt(50)
        .sum()
    )

    long_descriptions = (
        df["clean_description"]
        .str.len()
        .gt(10000)
        .sum()
    )

    html_remaining = (
        df["clean_description"]
        .str.contains(r"<.*?>", regex=True, na=False)
        .sum()
    )

    url_remaining = (
        df["clean_description"]
        .str.contains(r"http|www", regex=True, case=False, na=False)
        .sum()
    )

    statistics = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Duplicate Job IDs",
            "Empty Descriptions",
            "Descriptions < 50 Characters",
            "Descriptions > 10000 Characters",
            "HTML Remaining",
            "URLs Remaining",
            "Average Description Length",
            "Median Description Length",
            "Maximum Description Length",
            "Minimum Description Length"
        ],
        "Value": [
            total_rows,
            duplicate_job_ids,
            empty_descriptions,
            short_descriptions,
            long_descriptions,
            html_remaining,
            url_remaining,
            round(df["clean_description"].str.len().mean(), 2),
            df["clean_description"].str.len().median(),
            df["clean_description"].str.len().max(),
            df["clean_description"].str.len().min()
        ]
    })

    output_file = report_folder / "data_quality_report.csv"

    statistics.to_csv(output_file, index=False)

    print(statistics)

    print("\nReport Saved Successfully")
    print(output_file)


if __name__ == "__main__":
    main()