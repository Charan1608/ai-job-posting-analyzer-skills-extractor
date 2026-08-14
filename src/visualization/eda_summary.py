"""
==============================================================
EDA SUMMARY
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
==============================================================
"""

from pathlib import Path
import pandas as pd


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
        / "eda"
    )

    report_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("EDA SUMMARY")
    print("=" * 70)

    df = pd.read_csv(input_file)

    summary = pd.DataFrame({

        "Metric": [

            "Total Job Postings",
            "Unique Companies",
            "Unique Locations",
            "Unique Job Titles",
            "Unique Work Types",
            "Unique Industries"

        ],

        "Value": [

            len(df),

            df["company_name"].nunique()
            if "company_name" in df.columns else "Not Available",

            df["location"].nunique(),

            df["title"].nunique(),

            df["formatted_work_type"].nunique()
            if "formatted_work_type" in df.columns else "Not Available",

            df["industry_name"].nunique()
            if "industry_name" in df.columns else "Not Available"

        ]

    })

    print(summary)

    output_file = report_folder / "eda_summary.csv"

    summary.to_csv(output_file, index=False)

    print("\nEDA Summary Saved Successfully")
    print(output_file)


if __name__ == "__main__":
    main()