"""
=========================================================
CREATE GOLD STANDARD DATASET
=========================================================
"""

from pathlib import Path
import pandas as pd

print("=" * 70)
print("CREATE GOLD STANDARD DATASET")
print("=" * 70)

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "data" / "interim" / "business_analytics_postings.csv"

OUTPUT_FOLDER = ROOT / "data" / "labelled"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_FOLDER / "gold_standard_200.csv"

df = pd.read_csv(INPUT_FILE)

# Reproducible sample
gold = (
    df.sample(
        n=200,
        random_state=42
    )
    .copy()
)

# Annotation columns
gold["technical_skills"] = ""
gold["soft_skills"] = ""
gold["tools"] = ""
gold["certifications"] = ""
gold["experience"] = ""
gold["education"] = ""
gold["annotator"] = ""
gold["review_status"] = ""
gold["comments"] = ""

gold.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"Total Records : {len(df):,}")
print(f"Sample Size   : {len(gold)}")
print()
print("Saved Successfully")
print(OUTPUT_FILE)