"""
=========================================================
SKILL ANALYTICS
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
from collections import Counter
from itertools import combinations

import pandas as pd

from src.normalization.config import PROJECT_ROOT


NORMALIZED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


class SkillAnalytics:

    def __init__(self):

        print("=" * 60)
        print("SKILL ANALYTICS")
        print("=" * 60)

        self.df = pd.read_csv(NORMALIZED_FILE)

        print(f"Rows Loaded : {len(self.df):,}")

    # --------------------------------------------------------
    # Parse normalized skills
    # --------------------------------------------------------

    def parse_skills(self):

        parsed = []

        for value in self.df["normalized_technical_skills"]:

            if pd.isna(value):
                parsed.append([])
                continue

            try:
                parsed.append(ast.literal_eval(value))
            except Exception:
                parsed.append([])

        return parsed

    # --------------------------------------------------------
    # Skill Frequency
    # --------------------------------------------------------

    def skill_frequency(self):

        skills = self.parse_skills()

        counter = Counter()

        for job in skills:

            for skill in job:

                if skill["normalized"] is not None:

                    counter[skill["normalized"]] += 1

        output = (
            pd.DataFrame(
                counter.items(),
                columns=["skill", "frequency"]
            )
            .sort_values(
                "frequency",
                ascending=False
            )
        )

        output.to_csv(
            OUTPUT_FOLDER / "skill_frequency.csv",
            index=False
        )

        print()
        print("=" * 60)
        print("TOP 20 SKILLS")
        print("=" * 60)

        print(output.head(20))

    # --------------------------------------------------------
    # Skill Category Frequency
    # --------------------------------------------------------

    def category_frequency(self):

        skills = self.parse_skills()

        counter = Counter()

        for job in skills:

            for skill in job:

                if skill["skill_type"]:

                    counter[skill["skill_type"]] += 1

        output = (
            pd.DataFrame(
                counter.items(),
                columns=["category", "frequency"]
            )
            .sort_values(
                "frequency",
                ascending=False
            )
        )

        output.to_csv(
            OUTPUT_FOLDER / "skill_category_frequency.csv",
            index=False
        )

        print()
        print("=" * 60)
        print("TOP SKILL CATEGORIES")
        print("=" * 60)

        print(output.head(20))

    # --------------------------------------------------------
    # Company Skill Frequency
    # --------------------------------------------------------

    def company_skill_frequency(self):

        rows = []

        skills = self.parse_skills()

        for index, job in enumerate(skills):

            company = self.df.iloc[index]["company_name"]

            for skill in job:

                if skill["normalized"]:

                    rows.append(
                        [
                            company,
                            skill["normalized"]
                        ]
                    )

        output = (
            pd.DataFrame(
                rows,
                columns=[
                    "company",
                    "skill"
                ]
            )
            .value_counts()
            .reset_index(name="frequency")
        )

        output.to_csv(
            OUTPUT_FOLDER / "company_skill_frequency.csv",
            index=False
        )

        print()
        print("Company Skill Frequency exported.")

    # --------------------------------------------------------
    # Location Skill Frequency
    # --------------------------------------------------------

    def location_skill_frequency(self):

        rows = []

        skills = self.parse_skills()

        for index, job in enumerate(skills):

            location = self.df.iloc[index]["location"]

            for skill in job:

                if skill["normalized"]:

                    rows.append(
                        [
                            location,
                            skill["normalized"]
                        ]
                    )

        output = (
            pd.DataFrame(
                rows,
                columns=[
                    "location",
                    "skill"
                ]
            )
            .value_counts()
            .reset_index(name="frequency")
        )

        output.to_csv(
            OUTPUT_FOLDER / "location_skill_frequency.csv",
            index=False
        )

        print("Location Skill Frequency exported.")

    # --------------------------------------------------------
    # Skill Co-occurrence
    # --------------------------------------------------------

    def skill_pairs(self):

        counter = Counter()

        skills = self.parse_skills()

        for job in skills:

            current = sorted(
                list(
                    {
                        skill["normalized"]
                        for skill in job
                        if skill["normalized"]
                    }
                )
            )

            for pair in combinations(current, 2):

                counter[pair] += 1

        rows = []

        for pair, count in counter.items():

            rows.append(
                [
                    pair[0],
                    pair[1],
                    count
                ]
            )

        output = (
            pd.DataFrame(
                rows,
                columns=[
                    "skill_1",
                    "skill_2",
                    "frequency"
                ]
            )
            .sort_values(
                "frequency",
                ascending=False
            )
        )

        output.to_csv(
            OUTPUT_FOLDER / "skill_pairs.csv",
            index=False
        )

        print("Skill Pair Frequency exported.")


# --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    analytics = SkillAnalytics()

    analytics.skill_frequency()

    analytics.category_frequency()

    analytics.company_skill_frequency()

    analytics.location_skill_frequency()

    analytics.skill_pairs()

    print()
    print("=" * 60)
    print("ALL ANALYTICS EXPORTED")
    print("=" * 60)