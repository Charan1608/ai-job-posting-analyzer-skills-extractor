"""
=========================================================
SKILL CLEANER
AI-Powered Job Posting Analyzer
=========================================================
"""

import re
import unicodedata
import pandas as pd


class SkillCleaner:

    @staticmethod
    def clean(skill: str) -> str:
        """
        Standardize a skill before matching.

        Steps
        -----
        1. Handle null values
        2. Unicode normalization
        3. Lowercase
        4. Remove text inside brackets
        5. Replace separators
        6. Remove unwanted punctuation
        7. Remove extra whitespace
        """

        if pd.isna(skill):
            return ""

        skill = str(skill).strip()

        if not skill:
            return ""

        # Remove trademark symbols BEFORE Unicode normalization
        skill = (
            skill.replace("®", "")
                 .replace("™", "")
                 .replace("©", "")
        )

        # Unicode normalization
        skill = unicodedata.normalize("NFKC", skill)

        # Lowercase
        skill = skill.lower()

        # Remove text inside brackets
        skill = re.sub(r"\(.*?\)", " ", skill)

        # Normalize separators
        skill = (
            skill.replace("/", " ")
                 .replace("-", " ")
                 .replace("_", " ")
                 .replace("|", " ")
                 .replace(",", " ")
        )

        # Safety cleanup after Unicode normalization
        skill = (
            skill.replace("tm", "")
                 .replace("(r)", "")
                 .replace("(c)", "")
        )
        # Keep letters, numbers, spaces, +, # and .
        skill = re.sub(r"[^a-z0-9\s+#.]", " ", skill)

        # Remove extra spaces
        skill = re.sub(r"\s+", " ", skill).strip()

        # Remove trailing dots
        skill = skill.strip(".")

        return skill


if __name__ == "__main__":

    samples = [
        " Python ",
        "Power-BI",
        "MS Excel",
        "Machine-Learning",
        "SQL/PLSQL",
        "Python (Programming)",
        "C++",
        "Node.js",
        "Azure™",
        "Power BI®",
        "SQL_Server"
    ]

    for sample in samples:
        print(f"{sample:25} -> {SkillCleaner.clean(sample)}")