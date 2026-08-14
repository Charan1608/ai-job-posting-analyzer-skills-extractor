"""
=========================================================
SYNONYM MAPPER
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.cleaner import SkillCleaner
from src.normalization.config import PROJECT_ROOT


FILE = PROJECT_ROOT / "taxonomy" / "custom" / "synonyms.csv"


class SynonymMapper:

    def __init__(self):

        self.mapping = {}

        self.load()

    # --------------------------------------------------------
    # Load Synonym Dictionary
    # --------------------------------------------------------

    def load(self):

        if not FILE.exists():

            raise FileNotFoundError(
                f"Synonym dictionary not found:\n{FILE}"
            )

        df = pd.read_csv(FILE)

        required_columns = {
            "synonym",
            "canonical"
        }

        missing = required_columns - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        df = df.dropna(
            subset=[
                "synonym",
                "canonical"
            ]
        )

        df["synonym"] = (
            df["synonym"]
            .astype(str)
            .apply(SkillCleaner.clean)
        )

        df["canonical"] = (
            df["canonical"]
            .astype(str)
            .str.strip()
        )

        duplicate_count = (
            df["synonym"]
            .duplicated()
            .sum()
        )

        df = df.drop_duplicates(
            subset="synonym",
            keep="first"
        )

        self.mapping = dict(
            zip(
                df["synonym"],
                df["canonical"]
            )
        )

        print("=" * 60)
        print("SYNONYM MAPPER")
        print("=" * 60)
        print(f"Loaded Synonyms : {len(self.mapping):,}")
        print(f"Duplicate Entries : {duplicate_count}")

    # --------------------------------------------------------
    # Map Synonym
    # --------------------------------------------------------

    def map(self, skill):

        cleaned = SkillCleaner.clean(skill)

        if not cleaned:
            return ""

        return self.mapping.get(cleaned, cleaned)

    # --------------------------------------------------------
    # Check Existence
    # --------------------------------------------------------

    def exists(self, skill):

        cleaned = SkillCleaner.clean(skill)

        return cleaned in self.mapping


if __name__ == "__main__":

    mapper = SynonymMapper()

    samples = [

        "Python Programming",
        "Power BI Desktop",
        "MS Excel",
        "Business Analytics",
        "Python"

    ]

    print()

    for sample in samples:

        print(f"{sample:30} -> {mapper.map(sample)}")