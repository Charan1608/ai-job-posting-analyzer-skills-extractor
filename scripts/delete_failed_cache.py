from pathlib import Path
import pandas as pd

CACHE_DIR = Path("data/cache")

df = pd.read_csv("data/processed/sample_200_with_ai_skills.csv")

mask = (
    (df["technical_skills"] == "[]") &
    (df["tools"] == "[]") &
    (df["soft_skills"] == "[]") &
    (df["certifications"] == "[]")
)

failed = df.loc[mask, "job_id"]

deleted = 0

for job_id in failed:

    f = CACHE_DIR / f"{job_id}.json"

    if f.exists():
        f.unlink()
        deleted += 1

print("=" * 50)
print("FAILED CACHE REMOVAL")
print("=" * 50)
print("Jobs:", len(failed))
print("Deleted:", deleted)