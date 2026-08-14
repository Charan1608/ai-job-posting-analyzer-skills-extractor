"""
=========================================================
DATASET LOADER
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/labelled/gold_standard_1500.csv")


REQUIRED_COLUMNS = [
    "job_id",
    "description"
]


def load_dataset():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"{INPUT_FILE} not found."
        )

    df = pd.read_csv(INPUT_FILE)

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    print("=" * 60)
    print("DATASET LOADED")
    print("=" * 60)
    print(f"Rows : {len(df)}")

    return df


if __name__ == "__main__":

    df = load_dataset()

    print(df.head())