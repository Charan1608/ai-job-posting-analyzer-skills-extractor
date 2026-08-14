"""
=========================================================
NORMALIZATION EVALUATOR
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
import pandas as pd

from src.normalization.config import PROJECT_ROOT


NORMALIZED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)


class NormalizationEvaluator:

    def __init__(self):

        print("=" * 60)
        print("LOADING NORMALIZED DATASET")
        print("=" * 60)

        self.df = pd.read_csv(NORMALIZED_FILE)

        print(f"Rows Loaded : {len(self.df):,}")

    # --------------------------------------------------------
    # Parse Normalized Skill Column
    # --------------------------------------------------------

    def parse_column(self, column):

        parsed = []

        for value in self.df[column]:

            if pd.isna(value):

                parsed.append([])

                continue

            try:

                parsed.append(ast.literal_eval(value))

            except Exception:

                parsed.append([])

        return parsed

    # --------------------------------------------------------
    # Calculate Evaluation Metrics
    # --------------------------------------------------------

    def evaluate(self):

        skills = self.parse_column(
            "normalized_technical_skills"
        )

        total = 0
        matched = 0
        unmatched = 0

        method_counts = {}

        for job in skills:

            for skill in job:

                total += 1

                method = skill.get(
                    "method",
                    "unknown"
                )

                method_counts[method] = (
                    method_counts.get(method, 0) + 1
                )

                if skill["normalized"] is None:

                    unmatched += 1

                else:

                    matched += 1

        coverage = 0

        if total > 0:

            coverage = (
                matched / total
            ) * 100

        print()

        print("=" * 60)
        print("NORMALIZATION SUMMARY")
        print("=" * 60)

        print(f"Total Skills      : {total:,}")
        print(f"Matched Skills    : {matched:,}")
        print(f"Unmatched Skills  : {unmatched:,}")
        print(f"Coverage          : {coverage:.2f}%")

        print()

        print("=" * 60)
        print("MATCH METHOD DISTRIBUTION")
        print("=" * 60)

        for method, count in sorted(
            method_counts.items()
        ):

            print(f"{method:25}: {count}")

    # --------------------------------------------------------
    # Export Unmatched Skills
    # --------------------------------------------------------

    def export_unmatched_skills(self):

        skills = self.parse_column(
            "normalized_technical_skills"
        )

        unmatched = []

        for job in skills:

            for skill in job:

                if skill["normalized"] is None:

                    unmatched.append(
                        skill["original"]
                    )

        unmatched = sorted(
            set(unmatched)
        )

        output = pd.DataFrame(
            {
                "original_skill": unmatched
            }
        )

        output_file = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "unmatched_skills.csv"
        )

        output.to_csv(
            output_file,
            index=False
        )

        print()

        print("=" * 60)
        print("UNMATCHED SKILLS EXPORTED")
        print("=" * 60)

        print(
            f"Unique Unmatched Skills : {len(output):,}"
        )

        print(output_file)

       # --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    evaluator = NormalizationEvaluator()

    print()

    print("=" * 60)
    print("TEST PARSER")
    print("=" * 60)

    skills = evaluator.parse_column(
        "normalized_technical_skills"
    )

    print()

    print("First Job")

    print("-" * 60)

    for skill in skills[0]:

        print(skill)

        print()

    evaluator.evaluate()

    print()

    evaluator.export_unmatched_skills()