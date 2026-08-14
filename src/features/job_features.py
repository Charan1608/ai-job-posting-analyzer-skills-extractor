"""
=========================================================
JOB FEATURES
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.features.feature_utils import (
    experience_bucket,
    education_level,
    encode_work_type,
)


# --------------------------------------------------------
# Create Job Features
# --------------------------------------------------------

def create_job_features(row):
    """
    Create job-related features for ML.
    """

    features = {}

    # Experience
    features["experience_bucket"] = experience_bucket(
        row.get("experience", "")
    )

    # Education
    features["education_level"] = education_level(
        row.get("education", "")
    )

    # Work Type
    features["work_type_encoded"] = encode_work_type(
        row.get("work_type", "")
    )

    return features


# --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    sample = {
        "experience": "3+ years",
        "education": "Bachelor's Degree",
        "work_type": "FULL_TIME"
    }

    print(create_job_features(sample))