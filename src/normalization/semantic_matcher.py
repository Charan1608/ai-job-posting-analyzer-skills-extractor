"""
=========================================================
SEMANTIC MATCHER
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer

from src.normalization.cleaner import SkillCleaner
from src.normalization.abbreviation_mapper import AbbreviationMapper
from src.normalization.technology_mapper import TechnologyMapper
from src.normalization.synonym_mapper import SynonymMapper
from src.normalization.typo_mapper import TypoMapper

from src.normalization.config import (
    PROJECT_ROOT,
    EMBEDDING_MODEL,
    SEMANTIC_THRESHOLD
)


EMBEDDING_FILE = (
    PROJECT_ROOT
    / "models"
    / "embeddings"
    / "esco_embeddings.npy"
)

METADATA_FILE = (
    PROJECT_ROOT
    / "models"
    / "embeddings"
    / "esco_metadata.pkl"
)


class SemanticMatcher:

    def __init__(self, threshold=SEMANTIC_THRESHOLD):

        self.threshold = threshold

        print("=" * 60)
        print("LOADING SEMANTIC MATCHER")
        print("=" * 60)

        # ----------------------------------------------------
        # Validate Files
        # ----------------------------------------------------

        if not EMBEDDING_FILE.exists():

            raise FileNotFoundError(
                f"Embedding file not found:\n{EMBEDDING_FILE}"
            )

        if not METADATA_FILE.exists():

            raise FileNotFoundError(
                f"Metadata file not found:\n{METADATA_FILE}"
            )

        # ----------------------------------------------------
        # Load Embedding Model
        # ----------------------------------------------------

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        # ----------------------------------------------------
        # Load Cached Embeddings
        # ----------------------------------------------------

        self.embeddings = np.load(
            EMBEDDING_FILE
        )

        with open(
            METADATA_FILE,
            "rb"
        ) as f:

            self.metadata = pickle.load(f)

        # ----------------------------------------------------
        # Preprocessors
        # ----------------------------------------------------

        self.abbrev = AbbreviationMapper()

        self.technology = TechnologyMapper()

        self.synonyms = SynonymMapper()

        self.typos = TypoMapper()

        print(f"Embedding Model : {EMBEDDING_MODEL}")

        print(f"Embeddings      : {self.embeddings.shape}")

        print(f"Metadata Records: {len(self.metadata)}")

    # ----------------------------------------------------
    # Preprocess Skill
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
    # Generate Query Embedding
    # ----------------------------------------------------

    def encode(self, skill):

        query = self.model.encode(

            [skill],

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        return query[0]

    # ----------------------------------------------------
    # Retrieve Top Semantic Candidates
    # ----------------------------------------------------

    def retrieve_candidates(
        self,
        query_embedding,
        top_k=5
    ):

        scores = np.dot(

            self.embeddings,

            query_embedding

        )

        top_indices = np.argsort(

            scores

        )[::-1][:top_k]

        candidates = []

        for idx in top_indices:

            record = self.metadata[idx]

            score = float(scores[idx])

            candidates.append(

                {

                    "record": record,

                    "score": score

                }

            )

        return candidates

    # ----------------------------------------------------
    # Build Result Object
    # ----------------------------------------------------

    def build_result(

        self,

        original,

        record,

        score

    ):

        return {

            "original": original,

            "normalized": record["preferred_label"],

            "esco_uri": record["concept_uri"],

            "skill_type": record["skill_type"],

            "definition": record["definition"],

            "method": "semantic",

            "score": round(score, 4),

            "confidence": round(score, 4)

        }
        # ----------------------------------------------------
    # Main Semantic Matching
    # ----------------------------------------------------

    def match(self, skill, top_k=5):

        original = "" if skill is None else str(skill)

        # ------------------------------------------------
        # Preprocess
        # ------------------------------------------------

        skill = self.preprocess(skill)

        if not skill:

            return None

        # ------------------------------------------------
        # Encode Query
        # ------------------------------------------------

        query_embedding = self.encode(skill)

        # ------------------------------------------------
        # Retrieve Candidates
        # ------------------------------------------------

        candidates = self.retrieve_candidates(

            query_embedding,

            top_k=top_k

        )

        if not candidates:

            return None

        # ------------------------------------------------
        # Threshold Check
        # ------------------------------------------------

        best_candidate = candidates[0]

        if best_candidate["score"] < self.threshold:

            return None

        # ------------------------------------------------
        # Build Results
        # ------------------------------------------------

        results = []

        for candidate in candidates:

            results.append(

                self.build_result(

                    original=original,

                    record=candidate["record"],

                    score=candidate["score"]

                )

            )

        return results

    # ----------------------------------------------------
    # Best Match Only
    # ----------------------------------------------------

    def best_match(self, skill):

        results = self.match(skill, top_k=1)

        if results is None:

            return None

        return results[0]
    # --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    matcher = SemanticMatcher()

    tests = [

        "Artificial Intelligence",

        "Power BI",

        "Pyhton",

        "Business Analytics",

        "Machine Learnng",

        "SQL",

        "Tableau",

        "Tensor Flow",

        "Databricks",

        "Snow Flake",

        "MS Excel",

        "Power BI Desktop",

        "AWS",

        "Azure DevOps"

    ]

    print("\n" + "=" * 60)
    print("SEMANTIC MATCH TEST")
    print("=" * 60)

    for skill in tests:

        print("\n" + "-" * 60)
        print(f"Input : {skill}")

        results = matcher.match(skill)

        if results is None:

            print("No Match")

            continue

        for i, result in enumerate(results, start=1):

            print(f"\nCandidate {i}")

            print(f"Normalized : {result['normalized']}")
            print(f"Method     : {result['method']}")
            print(f"Score      : {result['score']}")
            print(f"Confidence : {result['confidence']}")
            print(f"ESCO URI   : {result['esco_uri']}")