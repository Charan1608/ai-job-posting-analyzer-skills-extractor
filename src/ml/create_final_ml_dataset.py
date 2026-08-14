"""
=========================================================
CREATE FINAL ML DATASET
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.config import PROJECT_ROOT


FEATURE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "feature_engineered_jobs_v2.csv"
)

ML_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ml_dataset.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_ml_dataset_v2.csv"
)


print("=" * 60)
print("CREATING FINAL ML DATASET")
print("=" * 60)

feature_df = pd.read_csv(FEATURE_FILE)

ml_df = pd.read_csv(ML_FILE)

print(f"Feature Rows : {len(feature_df)}")
print(f"ML Rows      : {len(ml_df)}")

# Keep only target column
target_df = ml_df[
    [
        "job_id",
        "standard_title"
    ]
]

final_df = feature_df.merge(

    target_df,

    on="job_id",

    how="left"

)

print()
print("Missing Targets :", final_df["standard_title"].isna().sum())

final_df.to_csv(

    OUTPUT_FILE,

    index=False

)

print()
print("=" * 60)
print("FINAL DATASET SAVED")
print("=" * 60)

print(OUTPUT_FILE)

print()
print(final_df.head())