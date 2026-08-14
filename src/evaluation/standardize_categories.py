"""
=========================================================
CATEGORY STANDARDIZATION ENGINE
=========================================================
"""

import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ground_truth_normalized_skills_long.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ground_truth_normalized_skills_long.csv"
)


# =====================================================
# MASTER CATEGORY RULES
# =====================================================

TOOL_KEYWORDS = {

    "power bi",
    "tableau",
    "excel",
    "microsoft excel",
    "aws",
    "amazon web services",
    "azure",
    "microsoft azure",
    "google cloud",
    "gcp",
    "oracle",
    "mysql",
    "postgresql",
    "sqlite",
    "duckdb",
    "mongodb",
    "snowflake",
    "databricks",
    "apache spark",
    "apache kafka",
    "apache hadoop",
    "apache airflow",
    "docker",
    "kubernetes",
    "git",
    "github",
    "gitlab",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "jupyter notebook",
    "jupyterlab",
    "vs code",
    "visual studio code",
    "pycharm",
    "sas",
    "spss"
}


SOFT_KEYWORDS = {

    "communication",
    "leadership",
    "teamwork",
    "team player",
    "collaboration",
    "problem solving",
    "solve problems",
    "critical thinking",
    "analytical thinking",
    "time management",
    "presentation",
    "presentation skills",
    "negotiation",
    "stakeholder management",
    "customer service",
    "interpersonal skills"
}


CERTIFICATION_KEYWORDS = {

    "certified",
    "certification",
    "pmp",
    "scrum master",
    "aws certified",
    "azure fundamentals",
    "microsoft certified",
    "google professional"
}


def decide_category(skill):

    skill = str(skill).strip().lower()

    if any(x in skill for x in CERTIFICATION_KEYWORDS):
        return "certification"

    if skill in TOOL_KEYWORDS:
        return "tool"

    if skill in SOFT_KEYWORDS:
        return "soft"

    # Everything else becomes technical
    return "technical"


def main():

    print("=" * 60)
    print("CATEGORY STANDARDIZATION")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    before = (
        df.groupby("normalized_skill")["skill_type"]
        .nunique()
        .gt(1)
        .sum()
    )

    print(f"Inconsistent Skills Before : {before}")

    df["skill_type"] = (
        df["normalized_skill"]
        .apply(decide_category)
    )

    after = (
        df.groupby("normalized_skill")["skill_type"]
        .nunique()
        .gt(1)
        .sum()
    )

    print(f"Inconsistent Skills After  : {after}")

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nSaved Successfully")


if __name__ == "__main__":

    main()