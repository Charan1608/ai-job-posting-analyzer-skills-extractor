"""
=========================================================
FEATURE UTILITIES
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
import pandas as pd

from src.normalization.config import PROJECT_ROOT


# --------------------------------------------------------
# File Paths
# --------------------------------------------------------

EXCLUDED_FILE = (
    PROJECT_ROOT
    / "taxonomy"
    / "custom"
    / "excluded_skills.csv"
)


# --------------------------------------------------------
# Load Excluded Skills
# --------------------------------------------------------

def load_excluded_skills():
    """
    Load excluded skills from CSV and return as a set.
    """

    df = pd.read_csv(EXCLUDED_FILE)

    return set(
        df["skill"]
        .dropna()
        .astype(str)
        .str.strip()
    )


# --------------------------------------------------------
# Parse Normalized Skills
# --------------------------------------------------------

def parse_skills(value):
    """
    Convert string representation of list into Python list.
    """

    if pd.isna(value):
        return []

    try:
        return ast.literal_eval(value)
    except Exception:
        return []


# --------------------------------------------------------
# Remove Excluded Skills
# --------------------------------------------------------

def filter_skills(skills):
    """
    Remove unwanted domain-specific skills.
    """

    excluded = load_excluded_skills()

    filtered = []

    for skill in skills:

        normalized = skill.get("normalized")

        if normalized is None:
            continue

        if str(normalized).strip() in excluded:
            continue

        filtered.append(skill)

    return filtered


# --------------------------------------------------------
# Experience Bucket
# --------------------------------------------------------

def experience_bucket(value):
    """
    Convert experience text into buckets.
    """

    value = str(value).lower()

    if any(x in value for x in ["0", "1", "entry", "fresher"]):
        return "Entry"

    elif any(x in value for x in ["2", "3"]):
        return "Junior"

    elif any(x in value for x in ["4", "5"]):
        return "Mid"

    elif any(x in value for x in ["6", "7", "8", "9"]):
        return "Senior"

    else:
        return "Expert"


# --------------------------------------------------------
# Education Level
# --------------------------------------------------------

def education_level(value):
    """
    Convert education text into categories.
    """

    value = str(value).lower()

    if "phd" in value or "doctor" in value:
        return "PhD"

    elif "master" in value or "mba" in value:
        return "Masters"

    elif "bachelor" in value:
        return "Bachelors"

    elif "diploma" in value:
        return "Diploma"

    else:
        return "Other"


# --------------------------------------------------------
# Work Type Encoding
# --------------------------------------------------------

def encode_work_type(value):
    """
    Convert work type into numeric encoding.
    """

    value = str(value).upper()

    mapping = {
        "FULL_TIME": 1,
        "CONTRACT": 2,
        "PART_TIME": 3,
        "INTERNSHIP": 4,
        "TEMPORARY": 5,
        "VOLUNTEER": 6,
        "OTHER": 7
    }

    return mapping.get(value, 0)


# --------------------------------------------------------
# Module Test
# --------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("FEATURE UTILITIES TEST")
    print("=" * 60)

    excluded = load_excluded_skills()

    print(f"Excluded Skills : {len(excluded)}")

    print(experience_bucket("2+ years"))

    print(education_level("Bachelor's Degree"))

    print(encode_work_type("FULL_TIME"))