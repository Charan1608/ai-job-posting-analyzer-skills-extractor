"""
=========================================================
NORMALIZATION STATISTICS
=========================================================
"""

import pandas as pd


def method_statistics(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count normalization methods.
    """
    return (
        long_df["method"]
        .value_counts(dropna=False)
        .rename_axis("method")
        .reset_index(name="count")
    )


def category_statistics(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count skill categories.
    """
    return (
        long_df["category"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("category")
        .reset_index(name="count")
    )


def skill_type_statistics(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Count technical/tool/soft/certification skills.
    """
    return (
        long_df["skill_type"]
        .value_counts()
        .rename_axis("skill_type")
        .reset_index(name="count")
    )


def top_skills(long_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Most common normalized skills.
    """
    return (
        long_df["normalized_skill"]
        .value_counts()
        .head(top_n)
        .rename_axis("normalized_skill")
        .reset_index(name="count")
    )


def confidence_statistics(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Confidence summary.
    """
    confidence = pd.to_numeric(
        long_df["confidence"],
        errors="coerce"
    )

    return pd.DataFrame({
        "Metric": [
            "Average",
            "Minimum",
            "Maximum",
            "Median"
        ],
        "Value": [
            confidence.mean(),
            confidence.min(),
            confidence.max(),
            confidence.median()
        ]
    })