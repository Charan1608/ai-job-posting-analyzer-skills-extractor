"""
=========================================================
MASTER SKILL NORMALIZER
AI-Powered Job Posting Analyzer
=========================================================
"""

from collections import Counter

from src.normalization.confidence_engine import ConfidenceEngine


class SkillNormalizer:

    def __init__(self):

        print("=" * 60)
        print("LOADING MASTER NORMALIZER")
        print("=" * 60)

        self.engine = ConfidenceEngine()

    # --------------------------------------------------------
    # Normalize One Skill
    # --------------------------------------------------------

    def normalize_skill(self, skill):

        if skill is None:

            return {

                "original": "",

                "normalized": None,

                "esco_uri": None,

                "skill_type": None,

                "definition": "",

                "method": "unmatched",

                "priority": 5,

                "confidence": 0.0,

                "reason": "Empty skill"

            }

        return self.engine.normalize(skill)

    # --------------------------------------------------------
    # Remove Duplicate Skills
    # --------------------------------------------------------

    def remove_duplicates(self, normalized_results):

        unique = {}

        for result in normalized_results:

            key = result["normalized"]

            if key is None:

                key = result["original"]

            if key not in unique:

                unique[key] = result

                continue

            if result["confidence"] > unique[key]["confidence"]:

                unique[key] = result

        return list(unique.values())
        # --------------------------------------------------------
    # Normalize List of Skills
    # --------------------------------------------------------

    def normalize_skills(self, skills):

        normalized_results = []

        for skill in skills:

            result = self.normalize_skill(skill)

            normalized_results.append(result)

        normalized_results = self.remove_duplicates(
            normalized_results
        )

        normalized_results = sorted(

            normalized_results,

            key=lambda x: (

                x["normalized"] is None,

                str(x["normalized"])

            )

        )

        return normalized_results

    # --------------------------------------------------------
    # Match Statistics
    # --------------------------------------------------------

    def statistics(self, normalized_results):

        total = len(normalized_results)

        matched = sum(

            1

            for r in normalized_results

            if r["normalized"] is not None

        )

        unmatched = total - matched

        coverage = (

            round((matched / total) * 100, 2)

            if total

            else 0

        )

        methods = Counter(

            r["method"]

            for r in normalized_results

        )

        return {

            "total_skills": total,

            "matched_skills": matched,

            "unmatched_skills": unmatched,

            "coverage_percent": coverage,

            "matching_methods": dict(methods)

        }
        # --------------------------------------------------------
    # Category Summary
    # --------------------------------------------------------

    def category_summary(self, normalized_results):

        categories = Counter(

            r["skill_type"]

            for r in normalized_results

            if r["skill_type"] is not None

        )

        return dict(categories)

    # --------------------------------------------------------
    # Average Confidence
    # --------------------------------------------------------

    def average_confidence(self, normalized_results):

        scores = [

            r["confidence"]

            for r in normalized_results

            if r["normalized"] is not None

        ]

        if not scores:

            return 0.0

        return round(

            sum(scores) / len(scores),

            4

        )

    # --------------------------------------------------------
    # Complete Normalization Report
    # --------------------------------------------------------

    def normalize(self, skills):

        normalized_results = self.normalize_skills(skills)

        report = {

            "normalized_skills": normalized_results,

            "statistics": self.statistics(
                normalized_results
            ),

            "category_summary": self.category_summary(
                normalized_results
            ),

            "average_confidence": self.average_confidence(
                normalized_results
            )

        }

        return report
    # --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    normalizer = SkillNormalizer()

    skills = [

        "Python",

        "Pyhton",

        "ML",

        "Artificial Intelligence",

        "Power BI",

        "Power BI Desktop",

        "Tensor Flow",

        "Machine Learnng",

        "Business Analytics",

        "SQL",

        "SQL",

        "Snow Flake",

        "Databricks",

        "MS Excel",

        None,

        ""

    ]

    report = normalizer.normalize(skills)

    print("\n" + "=" * 60)
    print("MASTER NORMALIZATION REPORT")
    print("=" * 60)

    print("\nNORMALIZED SKILLS\n")

    for result in report["normalized_skills"]:

        print("-" * 60)

        for key, value in result.items():

            print(f"{key:15}: {value}")

    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)

    for key, value in report["statistics"].items():

        print(f"{key:25}: {value}")

    print("\n" + "=" * 60)
    print("CATEGORY SUMMARY")
    print("=" * 60)

    for key, value in report["category_summary"].items():

        print(f"{key:25}: {value}")

    print("\n" + "=" * 60)

    print(
        f"Average Confidence : "
        f"{report['average_confidence']:.4f}"
    )