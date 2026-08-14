"""
=========================================================
PROJECT SETTINGS
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# -------------------------------------------------------
# Data Directories
# -------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CACHE_DATA_DIR = DATA_DIR / "cache"
LABELLED_DATA_DIR = DATA_DIR / "labelled"

# -------------------------------------------------------
# Report Directories
# -------------------------------------------------------

REPORTS_DIR = PROJECT_ROOT / "reports"
EDA_REPORTS_DIR = REPORTS_DIR / "eda"

# -------------------------------------------------------
# AI Directories
# -------------------------------------------------------

AI_DIR = PROJECT_ROOT / "src" / "ai"

PROMPTS_DIR = AI_DIR / "prompts"
CACHE_DIR = AI_DIR / "cache"

# -------------------------------------------------------
# Annotation
# -------------------------------------------------------

GOLD_STANDARD_FILE = LABELLED_DATA_DIR / "gold_standard_200.csv"

ANNOTATOR = "Charan N"

# -------------------------------------------------------
# LLM Configuration
# -------------------------------------------------------

MODEL_NAME = "llama-3.3-70b-versatile"

TEMPERATURE = 0

MAX_TOKENS = 4096