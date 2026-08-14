"""
=========================================================
ABBREVIATION MAPPER
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.cleaner import SkillCleaner
from src.normalization.config import PROJECT_ROOT


FILE = PROJECT_ROOT / "taxonomy" / "custom" / "abbreviations.csv"


class AbbreviationMapper:

    def __init__(self):

        self.mapping = {}

        self.load()

    # --------------------------------------------------------
    # Load Abbreviation Dictionary
    # --------------------------------------------------------

    def load(self):

        if not FILE.exists():

            raise FileNotFoundError(
                f"Abbreviation dictionary not found:\n{FILE}"
            )

        df = pd.read_csv(FILE)

        required_columns = {
            "abbreviation",
            "expanded"
        }

        missing = required_columns - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        df = df.dropna(subset=["abbreviation", "expanded"])

        df["abbreviation"] = (
            df["abbreviation"]
            .astype(str)
            .apply(SkillCleaner.clean)
        )

        df["expanded"] = (
            df["expanded"]
            .astype(str)
            .str.strip()
        )

        duplicate_count = (
            df["abbreviation"]
            .duplicated()
            .sum()
        )

        df = df.drop_duplicates(
            subset="abbreviation",
            keep="first"
        )

        self.mapping = dict(
            zip(
                df["abbreviation"],
                df["expanded"]
            )
        )

        print("=" * 60)
        print("ABBREVIATION MAPPER")
        print("=" * 60)
        print(f"Loaded Abbreviations : {len(self.mapping):,}")
        print(f"Duplicate Entries    : {duplicate_count}")

    # --------------------------------------------------------
    # Expand Abbreviation
    # --------------------------------------------------------

    def map(self, skill):

        cleaned = SkillCleaner.clean(skill)

        if not cleaned:
            return ""

        return self.mapping.get(cleaned, cleaned)


if __name__ == "__main__":

    mapper = AbbreviationMapper()

    samples = [
        "ML",
        "AI",
        "NLP",
        "BI",
        "AWS",
        "GCP",
        "PBI",
        "SQL",
        "Python"
    ]

    print()

    for sample in samples:

        print(f"{sample:10} -> {mapper.map(sample)}")