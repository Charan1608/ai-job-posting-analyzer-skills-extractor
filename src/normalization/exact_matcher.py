"""
=========================================================
EXACT ESCO MATCHER
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.normalization.taxonomy_loader import ESCOTaxonomy
from src.normalization.cleaner import SkillCleaner
from src.normalization.abbreviation_mapper import AbbreviationMapper
from src.normalization.technology_mapper import TechnologyMapper
from src.normalization.typo_mapper import TypoMapper
from src.normalization.synonym_mapper import SynonymMapper
from src.normalization.config import (
    EXACT_MATCH_SCORE,
    TECH_ALIAS_SCORE
)


class ExactMatcher:

    def __init__(self):

        self.taxonomy = ESCOTaxonomy()

        self.taxonomy.load()

        self.taxonomy.build_lookup()

        self.abbrev = AbbreviationMapper()

        self.technology = TechnologyMapper()

        self.synonyms = SynonymMapper()

        self.typos = TypoMapper()

    # --------------------------------------------------------
    # Exact Match Pipeline
    # --------------------------------------------------------

    def match(self, skill):

        original = "" if skill is None else str(skill)

        # ----------------------------------------------------
        # Step 1 : Clean Skill
        # ----------------------------------------------------
        skill = SkillCleaner.clean(skill)

        if not skill:
            return ""

        # Typo Mapping
        skill = self.typos.map(skill)

        # Abbreviation Mapping
        skill = self.abbrev.map(skill)

        # ----------------------------------------------------
        # Step 3 : Technology Mapping
        # ----------------------------------------------------

        tech = self.technology.match(skill)

        if tech is not None:

            skill = tech["normalized"]

        # ----------------------------------------------------
        # Step 4 : Synonym Mapping
        # ----------------------------------------------------

        skill = self.synonyms.map(skill)

        # ----------------------------------------------------
        # Step 5 : Preferred ESCO Match
        # ----------------------------------------------------

        lookup_key = skill.lower().strip()

        if lookup_key in self.taxonomy.lookup:

            record = self.taxonomy.lookup[lookup_key]

            return {

                "original": original,

                "normalized": record["preferred_label"],

                "esco_uri": record["concept_uri"],

                "skill_type": record["skill_type"],

                "definition": record["definition"],

                "method": "exact",

                "confidence": EXACT_MATCH_SCORE

            }

        # ----------------------------------------------------
        # Step 6 : Alternative Label Match
        # ----------------------------------------------------

        if lookup_key in self.taxonomy.alt_lookup:

            record = self.taxonomy.alt_lookup[lookup_key]

            return {

                "original": original,

                "normalized": record["preferred_label"],

                "esco_uri": record["concept_uri"],

                "skill_type": record["skill_type"],

                "definition": record["definition"],

                "method": "alt_label",

                "confidence": TECH_ALIAS_SCORE

            }

        # ----------------------------------------------------
        # No Match
        # ----------------------------------------------------

        return None


if __name__ == "__main__":

    matcher = ExactMatcher()

    tests = [

        "Pyhton",

        "Python",

        "Python Programming",

        "ML",

        "Power BI Desktop",

        "PowerBI",

        "MS Excel",

        "SQL",

        "Artificial Intelligence",

        "Business Analytics",

        "Tensor Flow",

        "Snowflake",

        "Databricks"

    ]

    print("\n" + "=" * 60)
    print("EXACT MATCH TEST RESULTS")
    print("=" * 60)

    for skill in tests:

        result = matcher.match(skill)

        print()

        if result:

            for key, value in result.items():

                print(f"{key:15}: {value}")

        else:

            print(f"{skill:20}: No Match")