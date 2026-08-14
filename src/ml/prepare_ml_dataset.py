"""
=========================================================
PREPARE MACHINE LEARNING DATASET
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.config import PROJECT_ROOT
from src.ml.title_standardizer import standardize_title


INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "feature_engineered_jobs.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ml_dataset.csv"
)


class PrepareMLDataset:

    def __init__(self):

        print("=" * 60)
        print("PREPARING ML DATASET")
        print("=" * 60)

        self.df = pd.read_csv(INPUT_FILE)

        print(f"Rows Loaded : {len(self.df):,}")

    # --------------------------------------------------------
    # Create Target Column
    # --------------------------------------------------------

    def create_target(self):

        print()
        print("=" * 60)
        print("CREATING TARGET COLUMN")
        print("=" * 60)

        self.df["standard_title"] = (
            self.df["title"]
            .apply(standardize_title)
        )

        print(
            self.df["standard_title"]
            .value_counts()
        )

    # --------------------------------------------------------
    # Composite Features
    # --------------------------------------------------------

    def create_composite_features(self):

        print()
        print("=" * 60)
        print("CREATING COMPOSITE FEATURES")
        print("=" * 60)

        self.df["analytics_score"] = (
            self.df["analytics"]
            + self.df["business_analysis"]
            + self.df["bi_tools"]
            + self.df["spreadsheet"]
        )

        self.df["data_engineering_score"] = (
            self.df["databases"]
            + self.df["cloud_tools"]
            + self.df["big_data"]
            + self.df["etl_tools"]
        )

        self.df["ai_readiness_score"] = (
            self.df["ai_skills"]
            + self.df["ml_skills"]
        )

        print("Composite features created.")

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    def save_dataset(self):

        self.df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print()
        print("=" * 60)
        print("ML DATASET SAVED")
        print("=" * 60)

        print(OUTPUT_FILE)


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    pipeline = PrepareMLDataset()

    pipeline.create_target()

    pipeline.create_composite_features()

    pipeline.save_dataset()