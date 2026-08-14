"""
=========================================================
NORMALIZATION QUALITY REPORT
=========================================================
"""

import pandas as pd


def build_quality_report(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build quality metrics for normalization.
    """

    total_skills = len(long_df)

    matched = long_df["normalized_skill"].notna().sum()

    unmatched = total_skills - matched

    avg_confidence = pd.to_numeric(
        long_df["confidence"],
        errors="coerce"
    ).mean()

    coverage = (
        matched / total_skills * 100
        if total_skills > 0
        else 0
    )

    method_dist = (
        long_df["method"]
        .value_counts(normalize=True)
        * 100
    )

    report = {
        "Metric": [
            "Total Skills",
            "Matched Skills",
            "Unmatched Skills",
            "Coverage %",
            "Average Confidence",
            "Technology Dictionary %",
            "Exact %",
            "Fuzzy %",
            "Semantic %",
            "Unmatched %"
        ],
        "Value": [
            total_skills,
            matched,
            unmatched,
            round(coverage, 2),
            round(avg_confidence, 4),

            round(method_dist.get("technology_dictionary", 0), 2),

            round(method_dist.get("exact", 0), 2),

            round(
                method_dist.get("fuzzy_preferred", 0)
                + method_dist.get("fuzzy_alt", 0),
                2
            ),

            round(method_dist.get("semantic", 0), 2),

            round(method_dist.get("unmatched", 0), 2)
        ]
    }

    return pd.DataFrame(report)