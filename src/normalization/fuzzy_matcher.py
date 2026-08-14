"""
=========================================================
RAPIDFUZZ MATCHER
AI-Powered Job Posting Analyzer
=========================================================
"""

from rapidfuzz import process, fuzz

from src.normalization.taxonomy_loader import ESCOTaxonomy
from src.normalization.cleaner import SkillCleaner
from src.normalization.abbreviation_mapper import AbbreviationMapper
from src.normalization.technology_mapper import TechnologyMapper
from src.normalization.synonym_mapper import SynonymMapper
from src.normalization.typo_mapper import TypoMapper
from src.normalization.config import (
    FUZZY_THRESHOLD
)


class FuzzyMatcher:

    def __init__(self, threshold=FUZZY_THRESHOLD):

        self.threshold = threshold

        self.taxonomy = ESCOTaxonomy()

        self.taxonomy.load()

        self.taxonomy.build_lookup()

        self.abbrev = AbbreviationMapper()

        self.technology = TechnologyMapper()

        self.synonyms = SynonymMapper()

        self.typos = TypoMapper()

        # ------------------------------------------------
        # Candidate Lists
        # ------------------------------------------------

        self.preferred_labels = list(
            self.taxonomy.lookup.keys()
        )

        self.alt_labels = list(
            self.taxonomy.alt_lookup.keys()
        )

    # ----------------------------------------------------
    # Skill Preprocessing
    # ----------------------------------------------------
    def preprocess(self, skill):

        skill = SkillCleaner.clean(skill)

        if not skill:
            return ""

        # Typo Mapping
        skill = self.typos.map(skill)

        # Abbreviation Mapping
        skill = self.abbrev.map(skill)

        # Technology Mapping
        tech = self.technology.match(skill)

        if tech is not None:
            skill = tech["normalized"]

        # Synonym Mapping
        skill = self.synonyms.map(skill)

        return skill.lower().strip()

    # ----------------------------------------------------
    # Build Result Object
    # ----------------------------------------------------

    def _build_result(
        self,
        original,
        record,
        score,
        method
    ):

        return {

            "original": original,

            "normalized": record["preferred_label"],

            "esco_uri": record["concept_uri"],

            "skill_type": record["skill_type"],

            "definition": record["definition"],

            "method": method,

            "score": round(score, 2),

            "confidence": round(score / 100, 2)

        }
        # ----------------------------------------------------
    # Preferred Label Matching
    # ----------------------------------------------------

    def _match_preferred(
        self,
        original,
        skill
    ):

        result = process.extractOne(

            skill,

            self.preferred_labels,

            scorer=fuzz.WRatio

        )

        if result is None:

            return None

        label, score, _ = result

        if score < self.threshold:

            return None

        record = self.taxonomy.lookup[label]

        return self._build_result(

            original=original,

            record=record,

            score=score,

            method="fuzzy_preferred"

        )

    # ----------------------------------------------------
    # Alternative Label Matching
    # ----------------------------------------------------

    def _match_alternative(
        self,
        original,
        skill
    ):

        result = process.extractOne(

            skill,

            self.alt_labels,

            scorer=fuzz.WRatio

        )

        if result is None:

            return None

        label, score, _ = result

        if score < self.threshold:

            return None

        record = self.taxonomy.alt_lookup[label]

        return self._build_result(

            original=original,

            record=record,

            score=score,

            method="fuzzy_alt"

        )
        # ----------------------------------------------------
    # Main Matching Function
    # ----------------------------------------------------

    def match(self, skill):

        original = "" if skill is None else str(skill)

        skill = self.preprocess(skill)

        if not skill:

            return None

        # ------------------------------------------------
        # Preferred Match
        # ------------------------------------------------

        preferred = self._match_preferred(

            original,

            skill

        )

        # ------------------------------------------------
        # Alternative Match
        # ------------------------------------------------

        alternative = self._match_alternative(

            original,

            skill

        )

        # ------------------------------------------------
        # Collect Candidates
        # ------------------------------------------------

        candidates = []

        if preferred is not None:

            candidates.append(preferred)

        if alternative is not None:

            candidates.append(alternative)

        # ------------------------------------------------
        # No Match
        # ------------------------------------------------

        if not candidates:

            return None

        # ------------------------------------------------
        # Return Highest Score
        # ------------------------------------------------

        best_match = max(

            candidates,

            key=lambda x: x["score"]

        )

        return best_match
    # --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    matcher = FuzzyMatcher()

    tests = [

        "Pyhton",

        "PowerBI",

        "Power BI Desktop",

        "Tableu",

        "Excell",

        "Machine Learnng",

        "Artificial Inteligence",

        "Business Analytic",

        "SQL",

        "Python",

        "Snow Flake",

        "Databrick",

        "MS Excel",

        "Power-BI"

    ]

    print("\n" + "=" * 60)
    print("RAPIDFUZZ MATCH TEST")
    print("=" * 60)

    for skill in tests:

        print("\n" + "-" * 60)

        print(f"Input : {skill}")

        result = matcher.match(skill)

        if result:

            print(f"Normalized : {result['normalized']}")
            print(f"Method     : {result['method']}")
            print(f"Score      : {result['score']}")
            print(f"Confidence : {result['confidence']}")

        else:

            print("No Match")