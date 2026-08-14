import ast
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sample_200_with_ai_skills.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "labelled"
    / "extraction_gold_30.csv"
)


def parse_list(value):
    if pd.isna(value):
        return []

    try:
        result = ast.literal_eval(str(value))

        if isinstance(result, list):
            return result

    except Exception:
        pass

    return []


df = pd.read_csv(INPUT_FILE)

# Select 30 postings using a fixed random seed
sample = df.sample(
    n=min(30, len(df)),
    random_state=42
).copy()

# Create human annotation columns
sample["gold_technical_skills"] = ""
sample["gold_tools"] = ""
sample["gold_certifications"] = ""

# Keep the LLM outputs separately for comparison
sample["llm_technical_skills"] = sample[
    "technical_skills"
].apply(parse_list)

sample["llm_tools"] = sample[
    "tools"
].apply(parse_list)

sample["llm_certifications"] = sample[
    "certifications"
].apply(parse_list)

# Keep only useful annotation columns
columns = [
    "job_id",
    "title",
    "description",
    "llm_technical_skills",
    "llm_tools",
    "llm_certifications",
    "gold_technical_skills",
    "gold_tools",
    "gold_certifications",
]

sample = sample[columns]

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

sample.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 70)
print("EXTRACTION GOLD SAMPLE CREATED")
print("=" * 70)

print(f"Source rows : {len(df)}")
print(f"Sample rows : {len(sample)}")
print(f"Output      : {OUTPUT_FILE}")

print()
print("Next step:")
print("Open extraction_gold_30.csv and manually fill:")
print()
print("gold_technical_skills")
print("gold_tools")
print("gold_certifications")
print()
print("Use Python-list format, for example:")
print('["Python", "SQL", "Power BI", "Tableau"]')