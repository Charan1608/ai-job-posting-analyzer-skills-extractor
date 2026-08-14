"""
=========================================================
CREATE REVIEW SHEET
AI-Powered Job Posting Analyzer
=========================================================
"""

import pandas as pd

# --------------------------------------------------------
# FILES
# --------------------------------------------------------

AI_FILE = "data/processed/sample_200_with_ai_skills.csv"

OUTPUT_FILE = "data/labelled/review_sheet.csv"

# --------------------------------------------------------
# LOAD
# --------------------------------------------------------

df = pd.read_csv(AI_FILE)

# --------------------------------------------------------
# KEEP ONLY IMPORTANT COLUMNS
# --------------------------------------------------------

review = df[
    [
        "job_id",
        "title",
        "company_name",
        "description",
        "technical_skills",
        "tools",
        "soft_skills",
        "certifications",
        "experience",
        "education",
    ]
].copy()

# --------------------------------------------------------
# ADD HUMAN REVIEW COLUMNS
# --------------------------------------------------------

review["reviewed_technical_skills"] = ""
review["reviewed_tools"] = ""
review["reviewed_soft_skills"] = ""
review["reviewed_certifications"] = ""

review["review_status"] = "Pending"

review["review_notes"] = ""

# --------------------------------------------------------
# SAVE
# --------------------------------------------------------

review.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("=" * 60)
print("REVIEW SHEET CREATED")
print("=" * 60)
print(f"Rows : {len(review)}")
print(f"Saved : {OUTPUT_FILE}")