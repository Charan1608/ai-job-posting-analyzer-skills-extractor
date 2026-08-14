"""
=========================================================
CONFIDENCE ENGINE
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.normalization.config import (
    FUZZY_THRESHOLD,
    SEMANTIC_THRESHOLD,
    EXACT_MATCH_SCORE,
    TECH_ALIAS_SCORE
)

from src.normalization.technology_mapper import TechnologyMapper
from src.normalization.exact_matcher import ExactMatcher
from src.normalization.fuzzy_matcher import FuzzyMatcher
from src.normalization.semantic_matcher import SemanticMatcher
from src.normalization.business_dictionary import BusinessDictionary


class ConfidenceEngine:

    def __init__(self):

        print("=" * 60)
        print("LOADING CONFIDENCE ENGINE")
        print("=" * 60)

        self.tech = TechnologyMapper()

        self.business = BusinessDictionary()

        self.exact = ExactMatcher()

        self.fuzzy = FuzzyMatcher(
            threshold=FUZZY_THRESHOLD
        )

        self.semantic = SemanticMatcher(
            threshold=SEMANTIC_THRESHOLD
        )

    # ----------------------------------------------------
    # Normalize Skill
    # ----------------------------------------------------

    def normalize(self, skill):

        original = "" if skill is None else str(skill)

               # ------------------------------------------------
        # Technology Dictionary
        # ------------------------------------------------

        tech = self.tech.match(original)

        if tech:

            return {

                "original": original,

                "normalized": tech["normalized"],

                "esco_uri": None,

                "skill_type": tech["category"],

                "definition": "",

                "method": "technology_dictionary",

                "priority": 1,

                "confidence": TECH_ALIAS_SCORE

            }

        # ------------------------------------------------
        # Business Analytics Dictionary
        # ------------------------------------------------

        business = self.business.match(original)

        if business:

            return {

                "original": original,

                "normalized": business["normalized"],

                "esco_uri": None,

                "skill_type": business["skill_type"],

                "definition": "",

                "method": "business_dictionary",

                "priority": 2,

                "confidence": 1.0,

                "reason": "Business Analytics Protected Dictionary"

            }

        # ------------------------------------------------
        # Exact Matcher
        # ------------------------------------------------

        exact = self.exact.match(original)

        if exact:

            exact["priority"] = 2

            return exact

        # ------------------------------------------------
        # Fuzzy Matcher
        # ------------------------------------------------

        fuzzy = self.fuzzy.match(original)

        if fuzzy:

            fuzzy["priority"] = 3

            return fuzzy

        # ------------------------------------------------
        # Semantic Matcher
        # ------------------------------------------------

        semantic = self.semantic.best_match(original)

        if semantic:

            semantic["priority"] = 4

            return semantic

        # ------------------------------------------------
        # Unmatched
        # ------------------------------------------------

        return {

            "original": original,

            "normalized": None,

            "esco_uri": None,

            "skill_type": None,

            "definition": "",

            "method": "unmatched",

            "priority": 5,

            "confidence": 0.0,

            "reason": "No suitable match found"

        }


if __name__ == "__main__":

    engine = ConfidenceEngine()

    tests = [

        "Python",

        "Power BI",

        "Tensor Flow",

        "Machine Learnng",

        "Business Analytics",

        "Pyhton",

        "SQL",

        "Artificial Intelligence",

        "Snowflake",

        "Tableau",

        "PowerBI",

        "MS Excel"

    ]

    print("\n" + "=" * 60)
    print("FINAL NORMALIZATION TEST")
    print("=" * 60)

    for skill in tests:

        print("\n" + "-" * 60)

        print(f"Input : {skill}")

        result = engine.normalize(skill)

        for key, value in result.items():

            print(f"{key:12}: {value}")