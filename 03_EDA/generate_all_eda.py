"""
=========================================================
Generate All EDA Charts
PGDBA Capstone Project
=========================================================
"""

import pandas as pd

from recruitment_analytics import generate_recruitment_analytics
from skills_analytics import generate_skills_analytics
from advanced_analytics import generate_advanced_analytics


def main():

    print("=" * 70)
    print("AI-Powered Job Posting Analyzer")
    print("Generating Recruitment Analytics Charts")
    print("=" * 70)

    DATASET = "data/processed/cleaned_postings.csv"

    df = pd.read_csv(DATASET)

    print(f"Dataset Loaded : {len(df):,} rows")

    generate_recruitment_analytics(df)
    generate_skills_analytics()
    generate_advanced_analytics()

    print()
    print("=" * 70)
    print("EDA Generation Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":
    main()