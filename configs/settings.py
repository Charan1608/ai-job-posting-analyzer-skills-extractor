"""
Project Configuration
"""

from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data folders
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

INTERIM_DATA_DIR = DATA_DIR / "interim"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

LABELLED_DATA_DIR = DATA_DIR / "labelled"

CACHE_DIR = DATA_DIR / "cache"

# Reports
REPORT_DIR = PROJECT_ROOT / "reports"

AUDIT_REPORT_DIR = REPORT_DIR / "audit"