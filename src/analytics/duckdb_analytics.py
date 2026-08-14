"""
=========================================================
DUCKDB ANALYTICS
AI-Powered Job Posting Analyzer
=========================================================
"""

import duckdb
import pandas as pd

from src.normalization.config import PROJECT_ROOT


NORMALIZED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)


class DuckDBAnalytics:

    def __init__(self):

        print("=" * 60)
        print("CONNECTING DUCKDB")
        print("=" * 60)

        self.connection = duckdb.connect()

        print("DuckDB initialized.")

    # --------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------

    def load_dataset(self):

        print()
        print("=" * 60)
        print("LOADING DATASET")
        print("=" * 60)

        df = pd.read_csv(NORMALIZED_FILE)

        print(f"Rows Loaded : {len(df):,}")

        self.connection.register("jobs", df)

    # --------------------------------------------------------
    # Dataset Summary
    # --------------------------------------------------------

    def dataset_summary(self):

        print()
        print("=" * 60)
        print("DATASET SUMMARY")
        print("=" * 60)

        total = self.connection.execute(
            """
            SELECT COUNT(*) FROM jobs
            """
        ).fetchone()[0]

        print(f"Total Jobs : {total}")

    # --------------------------------------------------------
    # Top Companies
    # --------------------------------------------------------

    def top_companies(self):

        print()
        print("=" * 60)
        print("TOP COMPANIES")
        print("=" * 60)

        result = self.connection.execute(
            """
            SELECT
                company_name,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY company_name
            ORDER BY jobs DESC
            LIMIT 10
            """
        ).fetchdf()

        print(result)

    # --------------------------------------------------------
    # Top Locations
    # --------------------------------------------------------

    def top_locations(self):

        print()
        print("=" * 60)
        print("TOP LOCATIONS")
        print("=" * 60)

        result = self.connection.execute(
            """
            SELECT
                location,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY location
            ORDER BY jobs DESC
            LIMIT 10
            """
        ).fetchdf()

        print(result)

    # --------------------------------------------------------
    # Top Job Titles
    # --------------------------------------------------------

    def top_titles(self):

        print()
        print("=" * 60)
        print("TOP JOB TITLES")
        print("=" * 60)

        result = self.connection.execute(
            """
            SELECT
                title,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY title
            ORDER BY jobs DESC
            LIMIT 10
            """
        ).fetchdf()

        print(result)

    # --------------------------------------------------------
    # Work Type Distribution
    # --------------------------------------------------------

    def work_type_distribution(self):

        print()
        print("=" * 60)
        print("WORK TYPE DISTRIBUTION")
        print("=" * 60)

        result = self.connection.execute(
            """
            SELECT
                work_type,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY work_type
            ORDER BY jobs DESC
            """
        ).fetchdf()

        print(result)

    # --------------------------------------------------------
    # Close Connection
    # --------------------------------------------------------

    def close(self):

        self.connection.close()

        print()
        print("DuckDB connection closed.")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    analytics = DuckDBAnalytics()

    analytics.load_dataset()

    analytics.dataset_summary()

    analytics.top_companies()

    analytics.top_locations()

    analytics.top_titles()

    analytics.work_type_distribution()

    analytics.close()