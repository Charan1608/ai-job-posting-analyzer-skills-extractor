"""
===========================================================
Job Title Explorer
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Purpose : Discover all job titles and their frequencies
===========================================================
"""

from pathlib import Path
import pandas as pd


def main():

    project_root = Path(__file__).resolve().parents[2]

    postings_file = project_root / "data" / "raw" / "postings.csv"

    output_folder = project_root / "reports" / "profiling"

    output_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("JOB TITLE EXPLORER")
    print("=" * 70)

    print("\nLoading postings.csv...")

    df = pd.read_csv(postings_file)

    print(f"Rows Loaded : {len(df):,}")

    # Verify required column exists
    if "title" not in df.columns:
        print("\n❌ ERROR: 'title' column not found.")
        print("Available columns:")
        print(df.columns.tolist())
        return

    title_frequency = (
        df["title"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts()
        .reset_index()
    )

    title_frequency.columns = ["Job Title", "Count"]

    output_file = output_folder / "job_title_frequency.csv"

    title_frequency.to_csv(output_file, index=False)

    print(f"\nUnique Job Titles : {len(title_frequency):,}")

    print("\nTop 20 Job Titles\n")

    print(title_frequency.head(20))

    print("\n✅ Report Saved")

    print(output_file)


if __name__ == "__main__":
    main()