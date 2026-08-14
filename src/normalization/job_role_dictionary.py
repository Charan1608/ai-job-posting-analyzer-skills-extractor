import pandas as pd

from src.normalization.config import PROJECT_ROOT


class JobRoleDictionary:

    def __init__(self):

        path = (
            PROJECT_ROOT
            / "taxonomy"
            / "job_role_dictionary.csv"
        )

        self.lookup = {}

        df = pd.read_csv(path)

        for _, row in df.iterrows():

            key = str(row["input"]).strip().lower()

            normalized = str(row["normalized_role"]).strip()

            self.lookup[key] = {

                "normalized_role": normalized,

                "method": "job_role_dictionary",

                "confidence": 1.0,

                "priority": 1

            }

        print("=" * 60)
        print("JOB ROLE DICTIONARY")
        print("=" * 60)
        print(f"Entries Loaded : {len(self.lookup)}")

    # --------------------------------------------------
    # Match Job Title
    # --------------------------------------------------

    def match(self, title):

        if title is None:
            return None

        title = str(title).strip().lower()

        # Exact Match
        if title in self.lookup:
            return self.lookup[title]

        # Partial Match
        for key, value in self.lookup.items():

            if key in title:
                return value

            if title in key:
                return value

        return None