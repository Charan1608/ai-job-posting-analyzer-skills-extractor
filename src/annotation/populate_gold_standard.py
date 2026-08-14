"""
=========================================================
POPULATE GOLD STANDARD
Copies AI extraction into working gold standard
=========================================================
"""

import pandas as pd

# ---------------------------------------------------------
# FILES
# ---------------------------------------------------------

GOLD_FILE = "data/labelled/gold_standard_200_working.csv"
AI_FILE = "data/processed/normalized_jobs.csv"

# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

gold = pd.read_csv(GOLD_FILE)
ai = pd.read_csv(AI_FILE)

# ---------------------------------------------------------
# INDEX BY JOB ID
# ---------------------------------------------------------

gold = gold.set_index("job_id")
ai = ai.set_index("job_id")

# ---------------------------------------------------------
# COLUMNS TO COPY
# ---------------------------------------------------------

columns = [
    "technical_skills",
    "tools",
    "soft_skills",
    "certifications",
    "experience",
    "education",
]

# ---------------------------------------------------------
# COPY VALUES
# ---------------------------------------------------------

for column in columns:

    gold[column] = ai[column]

# ---------------------------------------------------------
# RESET INDEX
# ---------------------------------------------------------

gold = gold.reset_index()

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

gold.to_csv(
    GOLD_FILE,
    index=False
)

print("=" * 60)
print("GOLD STANDARD UPDATED")
print("=" * 60)
print(f"Rows Updated : {len(gold)}")
print(f"Saved : {GOLD_FILE}")