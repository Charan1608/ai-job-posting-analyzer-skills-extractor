"""
=========================================================
FEATURE ENGINEERING PIPELINE
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.config import PROJECT_ROOT

from src.features.feature_utils import parse_skills
from src.features.skill_features import create_skill_features
from src.features.job_features import create_job_features


INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "feature_engineered_jobs.csv"
)


class FeatureEngineering:

    def __init__(self):

        print("=" * 60)
        print("FEATURE ENGINEERING")
        print("=" * 60)

        self.df = pd.read_csv(INPUT_FILE)

        print(f"Rows Loaded : {len(self.df):,}")
            # --------------------------------------------------------
    # Generate Feature Dataset
    # --------------------------------------------------------

    def generate_dataset(self):

        print()
        print("=" * 60)
        print("GENERATING FEATURES")
        print("=" * 60)

        feature_rows = []

        for _, row in self.df.iterrows():

            # Parse normalized skills
            skills = parse_skills(
                row["normalized_technical_skills"]
            )

            # Skill Features
            skill_features = create_skill_features(
                skills
            )

            # Job Features
            job_features = create_job_features(
                row
            )

            # Metadata
            feature_row = {

                "job_id": row["job_id"],
                "company_name": row["company_name"],
                "title": row["title"],
                "location": row["location"],

                **skill_features,

                **job_features
            }

            feature_rows.append(feature_row)

        self.features_df = pd.DataFrame(
            feature_rows
        )

        print()

        print(
            f"Features Created : {len(self.features_df):,}"
        )
            # --------------------------------------------------------
    # Save Dataset
    # --------------------------------------------------------

    def save_dataset(self):

        self.features_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print()

        print("=" * 60)
        print("FEATURE DATASET SAVED")
        print("=" * 60)

        print(OUTPUT_FILE)

        print()

        print(self.features_df.head())
        # --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    pipeline = FeatureEngineering()

    pipeline.generate_dataset()

    pipeline.save_dataset()