"""
=========================================================
TYPO MAPPER
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.normalization.cleaner import SkillCleaner


COMMON_TYPOS = {

    # Programming
    "pyhton": "python",
    "pythn": "python",

    # Machine Learning
    "machne learning": "machine learning",
    "machine learnng": "machine learning",
    "machine learing": "machine learning",

    # Artificial Intelligence
    "artificial inteligence": "artificial intelligence",

    # BI Tools
    "powerbi": "power bi",
    "power-bi": "power bi",
    "power bi desktop": "power bi",

    # Analytics
    "business analytic": "business analytics",

    # Excel
    "excell": "excel",
    "ms excell": "ms excel",

    # Tableau
    "tableu": "tableau",

    # Cloud
    "snow flake": "snowflake",

    # Databricks
    "databrick": "databricks",

    # TensorFlow
    "tensor flow": "tensorflow",

}


class TypoMapper:

    def __init__(self):

        self.mapping = {}

        for typo, corrected in COMMON_TYPOS.items():

            self.mapping[
                SkillCleaner.clean(typo)
            ] = SkillCleaner.clean(corrected)

        print("=" * 60)
        print("TYPO MAPPER")
        print("=" * 60)
        print(f"Loaded Common Typos : {len(self.mapping)}")

    def map(self, skill):

        skill = SkillCleaner.clean(skill)

        return self.mapping.get(skill, skill)


if __name__ == "__main__":

    mapper = TypoMapper()

    tests = [

        "Pyhton",

        "Machne Learning",

        "Machine Learnng",

        "PowerBI",

        "Power BI Desktop",

        "Artificial Inteligence",

        "Tableu",

        "Excell",

        "Snow Flake",

        "Databrick",

        "Tensor Flow"

    ]

    print()

    print("=" * 60)
    print("TYPO TEST")
    print("=" * 60)

    for skill in tests:

        print(f"{skill:30} -> {mapper.map(skill)}")
        