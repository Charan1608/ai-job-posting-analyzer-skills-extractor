"""
=========================================================
BATCH NORMALIZER
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import json
import pandas as pd

from src.normalization.pipeline import NormalizationPipeline


INPUT_FILE = Path(
    "data/processed/sample_200_with_ai_skills.csv"
)

OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "normalized_skills.csv"

SUMMARY_FILE = OUTPUT_DIR / "normalization_summary.csv"


class BatchNormalizer:

    def __init__(self):

        print("=" * 60)
        print("BATCH NORMALIZER")
        print("=" * 60)

        self.pipeline = NormalizationPipeline()

        self.stats = {
            "technology_dictionary": 0,
            "exact": 0,
            "alt_label": 0,
            "fuzzy_preferred": 0,
            "fuzzy_alt": 0,
            "semantic": 0,
            "unmatched": 0
        }

    def normalize_skill_list(self, skill_list):

        normalized = []

        if pd.isna(skill_list):

            return normalized

        try:

            skills = json.loads(skill_list)

        except:

            return normalized

        for skill in skills:

            result = self.pipeline.normalize(skill)

            self.stats[result["method"]] += 1

            normalized.append(result)

        return normalized

    def run(self):

        df = pd.read_csv(INPUT_FILE)

        print(f"Rows : {len(df):,}")

        df["normalized_results"] = df["technical_skills"].apply(
            self.normalize_skill_list
        )

        df.to_csv(OUTPUT_FILE, index=False)

        summary = pd.DataFrame(

            list(self.stats.items()),

            columns=["Method", "Count"]

        )

        summary["Percentage"] = (

            summary["Count"] /

            summary["Count"].sum() *

            100

        ).round(2)

        summary.to_csv(SUMMARY_FILE, index=False)

        print()

        print("=" * 60)
        print("DONE")
        print("=" * 60)

        print(f"Saved : {OUTPUT_FILE}")

        print(f"Saved : {SUMMARY_FILE}")

        print()

        print(summary)


if __name__ == "__main__":

    BatchNormalizer().run()