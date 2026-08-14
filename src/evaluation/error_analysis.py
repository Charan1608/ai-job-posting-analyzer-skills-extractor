"""
=========================================================
ERROR ANALYSIS
=========================================================
"""

from collections import Counter
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "evaluation_per_job.csv"
)

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


def split_skills(text):

    if pd.isna(text):
        return []

    text = str(text).strip()

    if text == "":
        return []

    return [x.strip() for x in text.split(",") if x.strip()]


def main():

    df = pd.read_csv(INPUT)

    fp_counter = Counter()
    fn_counter = Counter()

    for _, row in df.iterrows():

        fp = split_skills(row["false_positive_skills"])
        fn = split_skills(row["false_negative_skills"])

        fp_counter.update(fp)
        fn_counter.update(fn)

    fp_df = pd.DataFrame(
        fp_counter.items(),
        columns=["skill", "count"]
    ).sort_values(
        "count",
        ascending=False
    )

    fn_df = pd.DataFrame(
        fn_counter.items(),
        columns=["skill", "count"]
    ).sort_values(
        "count",
        ascending=False
    )

    fp_df.to_csv(
        OUTPUT / "top_false_positives.csv",
        index=False
    )

    fn_df.to_csv(
        OUTPUT / "top_false_negatives.csv",
        index=False
    )

    print("=" * 60)
    print("ERROR ANALYSIS COMPLETE")
    print("=" * 60)

    print("\nTop False Positives")
    print(fp_df.head(20))

    print("\nTop False Negatives")
    print(fn_df.head(20))


if __name__ == "__main__":
    main()