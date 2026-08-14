"""
=========================================================
SKILL FEATURES
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.features.feature_utils import filter_skills


def create_skill_features(skills):
    """
    Create numerical skill-based features for ML.
    """

    skills = filter_skills(skills)

    features = {}

    features["total_skills"] = len(skills)

    category_map = {
        "Programming Language": "programming_languages",
        "Database": "databases",
        "Database Language": "databases",
        "BI Tool": "bi_tools",
        "Cloud": "cloud_tools",
        "Cloud Data Warehouse": "cloud_tools",
        "Machine Learning": "ml_skills",
        "Artificial Intelligence": "ai_skills",
        "Big Data": "big_data",
        "Data Engineering": "data_engineering",
        "DevOps": "devops",
        "Version Control": "version_control",
        "ETL": "etl_tools",
        "Spreadsheet": "spreadsheet",
        "Analytics": "analytics",
        "Business Analysis": "business_analysis"
    }

    # Initialize all features
    for feature_name in set(category_map.values()):
        features[feature_name] = 0

    # Count categories
    for skill in skills:

        category = skill.get("skill_type")

        if category in category_map:

            features[category_map[category]] += 1

    # Skill diversity
    features["skill_diversity"] = sum(
        value > 0
        for value in features.values()
        if isinstance(value, int)
    )

    return features