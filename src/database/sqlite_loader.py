"""
=========================================================
SQLITE DATABASE LOADER
AI-Powered Job Posting Analyzer
=========================================================
"""

import sqlite3
import pandas as pd

from src.normalization.config import PROJECT_ROOT


DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "job_postings.db"
)

NORMALIZED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)


class SQLiteLoader:

    def __init__(self):

        print("=" * 60)
        print("CONNECTING SQLITE DATABASE")
        print("=" * 60)

        self.connection = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.connection.cursor()

        print(f"Database : {DATABASE_FILE}")

    # --------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------

    def load_dataset(self):

        print()
        print("=" * 60)
        print("LOADING NORMALIZED DATASET")
        print("=" * 60)

        df = pd.read_csv(NORMALIZED_FILE)

        print(f"Rows Loaded : {len(df):,}")

        return df

    # --------------------------------------------------------
    # Create Jobs Table
    # --------------------------------------------------------

    def create_jobs_table(self):

        print()
        print("=" * 60)
        print("CREATING JOBS TABLE")
        print("=" * 60)

        self.cursor.execute(
            """
            DROP TABLE IF EXISTS jobs
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE jobs (

                job_id TEXT PRIMARY KEY,

                company_name TEXT,

                title TEXT,

                location TEXT,

                work_type TEXT,

                experience TEXT,

                education TEXT,

                technical_skills TEXT,

                soft_skills TEXT,

                tools TEXT,

                certifications TEXT,

                normalized_technical_skills TEXT

            )
            """
        )

        self.connection.commit()

        print("Jobs table created successfully.")

    # --------------------------------------------------------
    # Insert Jobs
    # --------------------------------------------------------

    def insert_jobs(self):

        df = self.load_dataset()

        print()
        print("=" * 60)
        print("INSERTING JOBS")
        print("=" * 60)

        for _, row in df.iterrows():

            self.cursor.execute(
                """
                INSERT INTO jobs
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(row["job_id"]),
                    str(row["company_name"]),
                    str(row["title"]),
                    str(row["location"]),
                    str(row["work_type"]),
                    str(row["experience"]),
                    str(row["education"]),
                    str(row["technical_skills"]),
                    str(row["soft_skills"]),
                    str(row["tools"]),
                    str(row["certifications"]),
                    str(row["normalized_technical_skills"])
                )
            )

        self.connection.commit()

        print(f"Inserted {len(df):,} jobs.")

    # --------------------------------------------------------
    # Verify Database
    # --------------------------------------------------------

    def verify_database(self):

        print()
        print("=" * 60)
        print("VERIFY DATABASE")
        print("=" * 60)

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM jobs
            """
        )

        total = self.cursor.fetchone()[0]

        print(f"Total Jobs : {total:,}")

        print()

        self.cursor.execute(
            """
            SELECT
                job_id,
                company_name,
                title,
                location
            FROM jobs
            LIMIT 5
            """
        )

        rows = self.cursor.fetchall()

        print("First 5 Records")
        print("-" * 60)

        for row in rows:
            print(row)

    # --------------------------------------------------------
    # Close Connection
    # --------------------------------------------------------

    def close(self):

        self.connection.close()

        print()
        print("Database connection closed.")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    loader = SQLiteLoader()

    loader.create_jobs_table()

    loader.insert_jobs()

    loader.verify_database()

    loader.close()