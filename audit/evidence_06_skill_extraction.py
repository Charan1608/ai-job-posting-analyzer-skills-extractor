from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DATASET = ROOT / "data" / "processed" / "sample_200_with_ai_skills.csv"

print("=" * 80)
print("6. SKILL EXTRACTION – AI-ASSISTED SKILL IDENTIFICATION")
print("=" * 80)

df = pd.read_csv(DATASET)

print(f"\nDataset File       : {DATASET.name}")
print(f"Records Analysed   : {len(df):,}")
print(f"Total Columns      : {len(df.columns)}")

print("\n" + "=" * 80)
print("SKILL EXTRACTION FIELDS")
print("=" * 80)

skill_columns = [
    "skills_desc",
    "technical_skills",
    "soft_skills"
]

for col in skill_columns:
    if col in df.columns:
        non_null = df[col].notna().sum()
        print(f"{col:<22}: {non_null:,} non-null records")

print("\n" + "=" * 80)
print("SAMPLE EXTRACTED SKILLS")
print("=" * 80)

for i, (_, row) in enumerate(df.head(10).iterrows(), start=1):

    print(f"\nRecord {i}")
    print("-" * 80)

    print(f"Technical Skills : {str(row.get('technical_skills', ''))[:350]}")
    print(f"Soft Skills      : {str(row.get('soft_skills', ''))[:250]}")

print("\n" + "=" * 80)
print("EXTRACTION COVERAGE")
print("=" * 80)

technical_available = (
    df["technical_skills"].notna()
    & df["technical_skills"].astype(str).str.strip().ne("")
)

soft_available = (
    df["soft_skills"].notna()
    & df["soft_skills"].astype(str).str.strip().ne("")
)

both_available = technical_available & soft_available

print(f"Technical skill records : {technical_available.sum():,}")
print(f"Soft skill records      : {soft_available.sum():,}")
print(f"Both skill types        : {both_available.sum():,}")

print(
    f"Technical extraction coverage : "
    f"{technical_available.mean() * 100:.2f}%"
)

print(
    f"Soft-skill extraction coverage : "
    f"{soft_available.mean() * 100:.2f}%"
)

print("\n" + "=" * 80)
print("EXTRACTION METHOD")
print("=" * 80)

print(
    "Job-posting skill information was structured into "
    "technical and soft-skill fields for downstream "
    "normalization and feature engineering."
)

print("\n" + "=" * 80)
print("SKILL EXTRACTION EVIDENCE COMPLETE")
print("=" * 80)