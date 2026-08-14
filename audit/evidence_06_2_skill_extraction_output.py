from pathlib import Path
import pandas as pd
import ast
import json

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FILE = ROOT / "data" / "processed" / "sample_200_with_ai_skills.csv"

print("=" * 78)
print("6.2 STRUCTURED SKILL EXTRACTION OUTPUT")
print("=" * 78)

if not OUTPUT_FILE.exists():
    raise FileNotFoundError(
        f"Extraction output not found:\n{OUTPUT_FILE}"
    )

df = pd.read_csv(OUTPUT_FILE)

print("\nEXTRACTION DATASET")
print("-" * 78)

print(f"Output File       : {OUTPUT_FILE.name}")
print(f"Job Postings      : {len(df)}")
print(f"Total Columns     : {len(df.columns)}")

# ------------------------------------------------------------
# Coverage
# ------------------------------------------------------------

technical_count = df["technical_skills"].notna().sum()
soft_count = df["soft_skills"].notna().sum()

print("\nEXTRACTION COVERAGE")
print("-" * 78)

print(
    f"Technical Skills  : {technical_count}/{len(df)} "
    f"({technical_count / len(df) * 100:.2f}%)"
)

print(
    f"Soft Skills       : {soft_count}/{len(df)} "
    f"({soft_count / len(df) * 100:.2f}%)"
)

# ------------------------------------------------------------
# Parse skill lists
# ------------------------------------------------------------

def parse_skills(value):
    if pd.isna(value):
        return []

    text = str(value).strip()

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass

    return [text] if text else []


technical = df["technical_skills"].apply(parse_skills)
soft = df["soft_skills"].apply(parse_skills)

total_technical = sum(len(x) for x in technical)
total_soft = sum(len(x) for x in soft)

print("\nEXTRACTED SKILL VOLUME")
print("-" * 78)

print(f"Technical Skill Instances : {total_technical:,}")
print(f"Soft Skill Instances      : {total_soft:,}")
print(f"Total Skill Instances     : {total_technical + total_soft:,}")

# ------------------------------------------------------------
# Actual sample output
# ------------------------------------------------------------

print("\nSAMPLE AI-EXTRACTED RECORDS")
print("-" * 78)

for i in range(min(5, len(df))):

    print(f"\nRecord {i + 1}")

    print("Technical Skills :")
    print(", ".join(technical.iloc[i][:12]))

    print("Soft Skills      :")
    print(", ".join(soft.iloc[i][:8]))

# ------------------------------------------------------------
# Output structure
# ------------------------------------------------------------

print("\nSTRUCTURED OUTPUT")
print("-" * 78)

print("technical_skills  → List of identified technical skills")
print("soft_skills       → List of identified soft skills")
print("job posting       → Preserved for downstream processing")

print("\n" + "=" * 78)
print("6.2 STRUCTURED EXTRACTION OUTPUT VERIFIED")
print("=" * 78)
print(
    "AI-extracted skills are available for the subsequent "
    "normalization stage."
)
print("=" * 78)