"""
=========================================================
EVALUATION CONFIGURATION
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path

# -----------------------------
# INPUT FILES
# -----------------------------

GOLD_STANDARD = Path(
    "data/labelled/gold_standard_200.csv"
)

PREDICTIONS = Path(
    "data/processed/normalized_jobs.csv"
)

# -----------------------------
# OUTPUT DIRECTORY
# -----------------------------

OUTPUT_DIR = Path(
    "reports/evaluation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# -----------------------------
# OUTPUT FILES
# -----------------------------

SUMMARY_FILE = OUTPUT_DIR / "evaluation_summary.csv"

DETAIL_FILE = OUTPUT_DIR / "evaluation_results.csv"

CATEGORY_FILE = OUTPUT_DIR / "per_category_metrics.csv"

FALSE_POSITIVE_FILE = OUTPUT_DIR / "false_positives.csv"

FALSE_NEGATIVE_FILE = OUTPUT_DIR / "false_negatives.csv"

# -----------------------------
# SKILL COLUMNS
# -----------------------------

SKILL_COLUMNS = [
    "technical_skills",
    "tools",
    "soft_skills",
    "certifications"
]