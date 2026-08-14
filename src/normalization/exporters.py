"""
=========================================================
EXPORTERS
=========================================================
"""

import pandas as pd

from src.normalization.config import (
    OUTPUT_DIR,
    NORMALIZED_JOBS,
    NORMALIZED_SKILLS,
    SUMMARY_FILE,
    QUALITY_FILE,
    UNMATCHED_FILE,
)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_jobs(df: pd.DataFrame):

    df.to_csv(
        NORMALIZED_JOBS,
        index=False,
        encoding="utf-8"
    )


def save_long_table(df: pd.DataFrame):

    df.to_csv(
        NORMALIZED_SKILLS,
        index=False,
        encoding="utf-8"
    )


def save_summary(df: pd.DataFrame):

    df.to_csv(
        SUMMARY_FILE,
        index=False,
        encoding="utf-8"
    )


def save_quality(df: pd.DataFrame):

    df.to_csv(
        QUALITY_FILE,
        index=False,
        encoding="utf-8"
    )


def save_unmatched(df: pd.DataFrame):

    df.to_csv(
        UNMATCHED_FILE,
        index=False,
        encoding="utf-8"
    )