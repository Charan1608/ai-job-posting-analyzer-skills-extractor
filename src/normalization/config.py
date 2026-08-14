"""
=========================================================
NORMALIZATION CONFIG
=========================================================
"""

from pathlib import Path

# --------------------------------------------------------
# Paths
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "sample_200_with_ai_skills.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

# --------------------------------------------------------
# Output Files (AI)
# --------------------------------------------------------

NORMALIZED_JOBS = OUTPUT_DIR / "normalized_jobs.csv"

NORMALIZED_SKILLS = OUTPUT_DIR / "normalized_skills_long.csv"

SUMMARY_FILE = OUTPUT_DIR / "normalization_summary.csv"

QUALITY_FILE = OUTPUT_DIR / "normalization_quality.csv"

UNMATCHED_FILE = OUTPUT_DIR / "unmatched_skills.csv"

# --------------------------------------------------------
# Output Files (Ground Truth)
# --------------------------------------------------------

GT_NORMALIZED_JOBS = OUTPUT_DIR / "ground_truth_normalized_jobs.csv"

GT_NORMALIZED_SKILLS = OUTPUT_DIR / "ground_truth_normalized_skills_long.csv"

GT_SUMMARY_FILE = OUTPUT_DIR / "ground_truth_normalization_summary.csv"

GT_QUALITY_FILE = OUTPUT_DIR / "ground_truth_normalization_quality.csv"

GT_UNMATCHED_FILE = OUTPUT_DIR / "ground_truth_unmatched_skills.csv"

# --------------------------------------------------------
# Settings
# --------------------------------------------------------

CONFIDENCE_THRESHOLD = 0.75
# --------------------------------------------------------
# Matching Scores
# --------------------------------------------------------

EXACT_MATCH_SCORE = 1.00

ABBREVIATION_SCORE = 1.00

TECH_ALIAS_SCORE = 0.99

SYNONYM_SCORE = 0.98

# --------------------------------------------------------
# Matching Thresholds
# --------------------------------------------------------

FUZZY_THRESHOLD = 90

SEMANTIC_THRESHOLD = 0.75

# --------------------------------------------------------
# Embedding Model
# --------------------------------------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --------------------------------------------------------
# Random Seed
# --------------------------------------------------------

RANDOM_STATE = 42

# --------------------------------------------------------
# Future Database
# --------------------------------------------------------

DATABASE_FILE = PROJECT_ROOT / "database" / "jobs.duckdb"

# --------------------------------------------------------
# Reports
# --------------------------------------------------------

REPORT_DIR = PROJECT_ROOT / "reports"