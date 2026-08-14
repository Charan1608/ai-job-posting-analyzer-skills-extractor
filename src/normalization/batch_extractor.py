"""
=========================================================
BATCH AI EXTRACTION
AI-Powered Job Posting Analyzer
=========================================================
"""

import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from src.ai.extraction.extractor import SkillExtractor


INPUT_FILE = Path("data/labelled/gold_standard_200.csv")

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "sample_200_with_ai_skills.csv"


class BatchExtractor:

    def __init__(self):

        print("=" * 60)
        print("BATCH AI EXTRACTION")
        print("=" * 60)

        self.extractor = SkillExtractor()

    def run(self):

        df = pd.read_csv(INPUT_FILE)

        print(f"Records : {len(df)}")

        results = []

        for _, row in tqdm(df.iterrows(), total=len(df)):

            description = str(row["description"])

            try:

                extracted = self.extractor.extract(description)

            except Exception as e:

                print(f"Extraction Error : {e}")

                extracted = {

                    "technical_skills": [],

                    "soft_skills": [],

                    "tools": [],

                    "certifications": [],

                    "experience": "",

                    "education": ""

                }

            record = row.to_dict()

            record["technical_skills"] = json.dumps(
                extracted["technical_skills"]
            )

            record["soft_skills"] = json.dumps(
                extracted["soft_skills"]
            )

            record["tools"] = json.dumps(
                extracted["tools"]
            )

            record["certifications"] = json.dumps(
                extracted["certifications"]
            )

            record["experience"] = extracted["experience"]

            record["education"] = extracted["education"]

            results.append(record)

        output = pd.DataFrame(results)

        output.to_csv(OUTPUT_FILE, index=False)

        print()

        print("=" * 60)
        print("DONE")
        print("=" * 60)

        print(OUTPUT_FILE)


if __name__ == "__main__":

    BatchExtractor().run()