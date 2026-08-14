import json
from pathlib import Path

import pandas as pd

SOURCE = "data/labelled/gold_standard_200.csv"
CACHE_DIR = Path("data/cache")
OUTPUT = "data/processed/sample_200_with_ai_skills.csv"

# -------------------------------------------------
# Load original dataset
# -------------------------------------------------

df = pd.read_csv(SOURCE)

# Initialize extraction columns
for col in [
    "technical_skills",
    "soft_skills",
    "tools",
    "certifications",
]:
    df[col] = "[]"

df["experience"] = ""
df["education"] = ""

cache_count = 0

# -------------------------------------------------
# Populate from cache
# -------------------------------------------------

for cache_file in CACHE_DIR.glob("*.json"):

    # Ignore test file
    if cache_file.stem == "123456":
        continue

    job_id = int(cache_file.stem)

    with open(cache_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    mask = df["job_id"] == job_id

    if not mask.any():
        continue

    cache_count += 1

    df.loc[mask, "technical_skills"] = json.dumps(
        data.get("technical_skills", [])
    )

    df.loc[mask, "soft_skills"] = json.dumps(
        data.get("soft_skills", [])
    )

    df.loc[mask, "tools"] = json.dumps(
        data.get("tools", [])
    )

    df.loc[mask, "certifications"] = json.dumps(
        data.get("certifications", [])
    )

    df.loc[mask, "experience"] = data.get(
        "experience",
        ""
    )

    df.loc[mask, "education"] = data.get(
        "education",
        ""
    )

# -------------------------------------------------
# Save
# -------------------------------------------------

df.to_csv(
    OUTPUT,
    index=False
)

print("=" * 60)
print("REBUILD COMPLETE")
print("=" * 60)
print(f"Dataset Rows : {len(df)}")
print(f"Recovered Cache Jobs : {cache_count}")

remaining = len(df) - cache_count

print(f"Pending Jobs : {remaining}")
print(f"Saved To : {OUTPUT}")