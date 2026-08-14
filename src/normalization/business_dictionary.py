"""
=========================================================
Business Analytics Dictionary
=========================================================
"""

import pandas as pd

from src.normalization.config import PROJECT_ROOT


# --------------------------------------------------------
# Training Taxonomy Category Mapping
#
# The CSV's own `skill_type` column only ever holds one of
# three generic ESCO-style values: "knowledge",
# "skill/competence", "tool". None of those match the
# category taxonomy the ML model was trained on (see
# `CATEGORIES` in feature_engineering_v2.py: "Business
# Analysis", "Analytics", "Machine Learning", "Programming
# Language", "Database Language", "BI Tool", "Spreadsheet",
# "Cloud", etc.).
#
# Because FeatureEngineeringV2._category_features_for_job()
# only increments a category counter when
# `category in counts` (counts being keyed by that training
# taxonomy), every business-dictionary match was silently
# contributing to NONE of the category features -- it always
# fell through untouched.
#
# This map translates each dictionary entry's `normalized`
# skill name to the correct training-taxonomy category, so
# skills sourced from this dictionary count the same way
# skills from the technology dictionary already do.
#
# Keyed by the exact `normalized` value in the CSV
# (lowercase). Update this whenever a new row is added to
# business_analytics_dictionary.csv.
# --------------------------------------------------------

CATEGORY_BY_NORMALIZED = {

    "business analysis": "Business Analysis",
    "analyse business requirements": "Business Analysis",
    "manage stakeholders": "Business Analysis",
    "communicate with stakeholders": "Business Analysis",
    "dashboard development": "Business Analysis",
    "prepare reports": "Business Analysis",

    "data analysis": "Analytics",
    "statistics": "Analytics",

    "machine learning": "Machine Learning",

    "python": "Programming Language",

    "sql": "Database Language",

    "power bi": "BI Tool",
    "tableau": "BI Tool",

    "microsoft excel": "Spreadsheet",

    "microsoft azure": "Cloud",
    "amazon web services": "Cloud",

}


class BusinessDictionary:

    def __init__(self):

        path = (
            PROJECT_ROOT
            / "taxonomy"
            / "business_analytics_dictionary.csv"
        )

        self.lookup = {}

        df = pd.read_csv(path)

        unmapped = set()

        for _, row in df.iterrows():

            key = str(row["input"]).strip().lower()

            normalized = str(row["normalized"]).strip()

            esco_skill_type = row["skill_type"]

            # Translate to the training taxonomy. Fall back to the
            # raw CSV value (and flag it) if a row was added to the
            # CSV without a corresponding entry here -- this keeps
            # the pipeline running instead of crashing, but the
            # printed warning below makes the gap visible immediately
            # instead of silently zeroing out that skill's category
            # features again.
            training_category = CATEGORY_BY_NORMALIZED.get(
                normalized.lower()
            )

            if training_category is None:
                unmapped.add(normalized)
                training_category = esco_skill_type

            self.lookup[key] = {

                "normalized": normalized,

                "skill_type": training_category,

                # Kept for debugging/traceability -- the original
                # ESCO-style type from the CSV, before translation.
                "esco_skill_type": esco_skill_type,

                "method": "business_dictionary",

                "confidence": 1.0,

                "priority": 1

            }

        print("=" * 60)
        print("BUSINESS ANALYTICS DICTIONARY")
        print("=" * 60)
        print(f"Entries Loaded : {len(self.lookup)}")

        if unmapped:

            print()
            print(
                "WARNING: the following normalized skills have no "
                "entry in CATEGORY_BY_NORMALIZED and are falling "
                "back to their raw CSV skill_type (they will NOT "
                "count toward any ML category feature until mapped):"
            )

            for name in sorted(unmapped):
                print(f"  - {name}")

    # ----------------------------------------------------
    # Match Skill
    # ----------------------------------------------------

    def match(self, skill):

        if skill is None:
            return None

        skill = str(skill).strip().lower()

        # Exact Match
        if skill in self.lookup:
            return self.lookup[skill]

        # Partial Match
        for key, value in self.lookup.items():

            if key in skill:
                return value

            if skill in key:
                return value

        return None