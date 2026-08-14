"""
=========================================================
TECHNOLOGY MAPPER
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.cleaner import SkillCleaner
from src.normalization.config import PROJECT_ROOT


FILE = PROJECT_ROOT / "taxonomy" / "custom" / "technology_dictionary.csv"


class TechnologyMapper:

    def __init__(self):

        self.mapping = {}

        self.load()

    # --------------------------------------------------------
    # Load Technology Dictionary
    # --------------------------------------------------------

    def load(self):

        if not FILE.exists():

            raise FileNotFoundError(
                f"Technology dictionary not found:\n{FILE}"
            )

        df = pd.read_csv(FILE)

        required_columns = {
            "technology",
            "canonical",
            "category"
        }

        missing = required_columns - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        df = df.dropna(
            subset=[
                "technology",
                "canonical",
                "category"
            ]
        )

        df["technology"] = (
            df["technology"]
            .astype(str)
            .apply(SkillCleaner.clean)
        )

        df["canonical"] = (
            df["canonical"]
            .astype(str)
            .str.strip()
        )

        df["category"] = (
            df["category"]
            .astype(str)
            .str.strip()
        )

        duplicate_count = (
            df["technology"]
            .duplicated()
            .sum()
        )

        df = df.drop_duplicates(
            subset="technology",
            keep="first"
        )

        self.mapping = {}

        for _, row in df.iterrows():

            self.mapping[row["technology"]] = {

                "normalized": row["canonical"],

                "category": row["category"]

            }

        print("=" * 60)
        print("TECHNOLOGY MAPPER")
        print("=" * 60)
        print(f"Loaded Technologies : {len(self.mapping):,}")
        print(f"Duplicate Entries   : {duplicate_count}")

    # --------------------------------------------------------
    # Match Technology
    # --------------------------------------------------------

    def match(self, skill):

        cleaned = SkillCleaner.clean(skill)

        if not cleaned:
            return None

        return self.mapping.get(cleaned)

    # --------------------------------------------------------
    # Check Existence
    # --------------------------------------------------------

    def exists(self, skill):

        cleaned = SkillCleaner.clean(skill)

        return cleaned in self.mapping


if __name__ == "__main__":

    mapper = TechnologyMapper()

    tests = [

        "JIRA",

        "Azure DevOps",

        "SAP FICO",

        "VLOOKUP",

        "Pivot tables",

        "Microsoft Office",

        "Power Query",

        "DAX",

        "SSIS",

        "Power BI",

        "Python"

    ]

    print("\nTEST RESULTS\n")

    for skill in tests:

        print(skill)

        print(mapper.match(skill))

        print("-" * 50)