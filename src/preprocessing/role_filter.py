"""
==============================================================
Role Filter
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Version : 1.0
Purpose : Filter Business Analytics related job postings
==============================================================
"""

from pathlib import Path
import pandas as pd
import yaml


def load_config(config_file):
    """Load YAML configuration."""
    with open(config_file, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def contains_keyword(text, keywords):
    """Check if any keyword exists in text."""
    text = str(text).lower()

    for keyword in keywords:
        if keyword in text:
            return True

    return False


def main():

    project_root = Path(__file__).resolve().parents[2]

    postings_file = project_root / "data" / "raw" / "postings.csv"

    config_file = project_root / "configs" / "roles" / "target_roles.yaml"

    output_folder = project_root / "data" / "interim"

    output_folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("ROLE FILTER")
    print("=" * 70)

    print("\nLoading dataset...")

    df = pd.read_csv(postings_file)

    config = load_config(config_file)

    include_keywords = config["project_scope"]["include_keywords"]

    exclude_keywords = config["project_scope"]["exclude_keywords"]

    print(f"Original Records : {len(df):,}")

    include_mask = df["title"].apply(
        lambda x: contains_keyword(x, include_keywords)
    )

    exclude_mask = df["title"].apply(
        lambda x: contains_keyword(x, exclude_keywords)
    )

    filtered_df = df[include_mask & ~exclude_mask].copy()

    output_file = output_folder / "business_analytics_postings.csv"

    filtered_df.to_csv(output_file, index=False)

    print(f"Filtered Records : {len(filtered_df):,}")

    print("\nSaved Successfully")

    print(output_file)


if __name__ == "__main__":
    main()