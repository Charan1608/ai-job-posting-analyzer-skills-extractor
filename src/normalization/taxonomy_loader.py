"""
=========================================================
ESCO TAXONOMY LOADER
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

from src.normalization.config import PROJECT_ROOT

ESCO_FILE = PROJECT_ROOT / "taxonomy" / "esco" / "skills.csv"


class ESCOTaxonomy:

    def __init__(self):

        self.skills = None

        self.lookup = {}

        self.alt_lookup = {}

    # --------------------------------------------------------
    # Load ESCO Taxonomy
    # --------------------------------------------------------

    def load(self):

        if not ESCO_FILE.exists():

            raise FileNotFoundError(
                f"ESCO taxonomy not found:\n{ESCO_FILE}"
            )

        self.skills = pd.read_csv(ESCO_FILE)

        required_columns = {
            "preferredLabel",
            "conceptUri",
            "altLabels",
            "definition",
            "skillType"
        }

        missing = required_columns - set(self.skills.columns)

        if missing:

            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        print("=" * 60)
        print("ESCO TAXONOMY")
        print("=" * 60)

        print(f"Skills Loaded : {len(self.skills):,}")

        return self.skills

    # --------------------------------------------------------
    # Build Lookup Dictionaries
    # --------------------------------------------------------

    def build_lookup(self):

        if self.skills is None:
            self.load()

        self.lookup = {}
        self.alt_lookup = {}

        duplicate_count = 0

        for _, row in self.skills.iterrows():

            preferred_label = (
                ""
                if pd.isna(row["preferredLabel"])
                else str(row["preferredLabel"]).strip()
            )

            if not preferred_label:
                continue

            record = {
                "preferred_label": preferred_label,
                "concept_uri": row["conceptUri"],
                "skill_type": row["skillType"],
                "definition": (
                    ""
                    if pd.isna(row["definition"])
                    else str(row["definition"]).strip()
                )
            }

            preferred = preferred_label.lower()

            if preferred in self.lookup:
                duplicate_count += 1

            self.lookup[preferred] = record

            if pd.notna(row["altLabels"]):

                labels = (
                    str(row["altLabels"])
                    .replace("\r", "")
                    .split("\n")
                )

                for label in labels:

                    label = label.strip().lower()

                    if label:
                        self.alt_lookup[label] = record

        print(f"Preferred Skills : {len(self.lookup):,}")
        print(f"Alternative Names: {len(self.alt_lookup):,}")
        print(f"Duplicate Labels : {duplicate_count}")
        print(f"Unique Concepts  : {self.skills['conceptUri'].nunique():,}")
        print(f"Skill Types      : {self.skills['skillType'].nunique()}")

        return self.lookup


if __name__ == "__main__":

    taxonomy = ESCOTaxonomy()

    taxonomy.load()

    taxonomy.build_lookup()

    print()

    sample = taxonomy.lookup.get("machine learning")

    print(sample)