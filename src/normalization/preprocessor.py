"""
=========================================================
NORMALIZATION PREPROCESSOR
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.normalization.cleaner import SkillCleaner
from src.normalization.abbreviation_mapper import AbbreviationMapper
from src.normalization.synonym_mapper import SynonymMapper


class SkillPreprocessor:

    def __init__(self):

        self.abbrev = AbbreviationMapper()
        self.synonyms = SynonymMapper()

    def process(self, skill):

        if skill is None:
            return ""

        skill = SkillCleaner.clean(skill)
        skill = self.abbrev.map(skill)
        skill = self.synonyms.map(skill)

        return skill


if __name__ == "__main__":

    processor = SkillPreprocessor()

    tests = [

        "Python Programming",

        "Power BI Desktop",

        "ML",

        "Business Analytics",

        "Tensor Flow",

        "Pyhton"

    ]

    print("=" * 60)
    print("PREPROCESSOR TEST")
    print("=" * 60)

    for skill in tests:

        print(f"{skill:30} -> {processor.process(skill)}")