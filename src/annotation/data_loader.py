"""
=========================================================
DATA LOADER
AI Job Skill Annotation Tool
=========================================================
"""

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Dataset Path
# ---------------------------------------------------------

DATA_FILE = Path("data/labelled/gold_standard_200_working.csv")


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

def load_dataset():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    return df


# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

def save_dataset(df):

    df.to_csv(
        DATA_FILE,
        index=False
    )