"""
=========================================================
NORMALIZATION PIPELINE
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
from pathlib import Path

import pandas as pd

from src.normalization.confidence_engine import ConfidenceEngine
from src.normalization.job_role_dictionary import JobRoleDictionary
from src.normalization.config import PROJECT_ROOT

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sample_200_with_ai_skills.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

NORMALIZED_JOBS = OUTPUT_DIR / "normalized_jobs.csv"

NORMALIZED_SKILLS = OUTPUT_DIR / "normalized_skills_long.csv"

SUMMARY_FILE = OUTPUT_DIR / "normalization_summary.csv"

QUALITY_FILE = OUTPUT_DIR / "normalization_quality.csv"

UNMATCHED_FILE = OUTPUT_DIR / "unmatched_skills.csv"


class NormalizationPipeline:

    def __init__(self):

        print("=" * 60)
        print("INITIALIZING NORMALIZATION PIPELINE")
        print("=" * 60)

        self.engine = ConfidenceEngine()
        self.role_engine = JobRoleDictionary()

    # --------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------

    def load_dataset(self):

        print()
        print("=" * 60)
        print("LOADING DATASET")
        print("=" * 60)

        df = pd.read_csv(INPUT_FILE)

        print(f"Rows Loaded : {len(df):,}")

        return df

    # --------------------------------------------------------
    # Parse AI Skill List
    # --------------------------------------------------------

    def parse_skill_list(self, value):

        if pd.isna(value):
            return []

        value = str(value).strip()

        if value == "":
            return []

        try:

            skills = ast.literal_eval(value)

            if isinstance(skills, list):
                return skills

        except Exception:
            pass

        return []

    # --------------------------------------------------------
    # Normalize a Single Skill
    # --------------------------------------------------------

    def normalize(self, skill):

        return self.engine.normalize(skill)

    # --------------------------------------------------------
    # Normalize a List of Skills
    # --------------------------------------------------------

    def normalize_list(self, skills):

        results = []

        for skill in skills:

            results.append(self.normalize(skill))

        return results

    # --------------------------------------------------------
    # Normalize Single Job
    # --------------------------------------------------------

    def normalize_job(self, extracted):

        normalized = {}

        normalized["technical_skills"] = self.normalize_list(
            extracted["technical_skills"]
        )

        normalized["soft_skills"] = extracted["soft_skills"]

        # Keep the raw tool name strings under "tools" -- unchanged,
        # since existing UI components (e.g. the "Tools Used" chart)
        # already read this as a flat list of strings.
        normalized["tools"] = extracted["tools"]

        # ALSO normalize the same tools into the same
        # {original, normalized, skill_type, ...} shape used for
        # technical_skills. Previously "tools" was passed straight
        # through as raw strings and never reached ConfidenceEngine,
        # so entries like Python/SQL/Power BI/Excel/Azure never got a
        # skill_type and never made it into what was sent to the ML
        # model or the skill-gap engine -- they'd show up as
        # "missing skills" even when clearly present. This gives
        # callers (app.py) a normalized version to merge in for
        # prediction / skill-gap purposes, without disturbing the
        # existing "tools" key's shape.
        normalized["tools_normalized"] = self.normalize_list(
            extracted["tools"]
        )

        normalized["certifications"] = extracted["certifications"]

        normalized["experience"] = extracted["experience"]

        normalized["education"] = extracted["education"]

        return normalized

    # --------------------------------------------------------
    # Normalize JSON Skill Column
    # --------------------------------------------------------

    def normalize_column(self, value):

        skills = self.parse_skill_list(value)

        results = []

        for skill in skills:

            results.append(
                self.normalize(skill)
            )

        return results

    # --------------------------------------------------------
    # Normalize Entire Dataset
    # --------------------------------------------------------

    def process_dataset(self, df):

        normalized_rows = []
        normalized_roles = []

        for index, row in df.iterrows():

            # Normalize technical skills
            normalized = self.normalize_column(
                row["technical_skills"]
            )

            normalized_rows.append(normalized)

            # Normalize job role
            role = self.role_engine.match(
                row["title"]
            )

            if role is not None:
                normalized_roles.append(
                    role["normalized_role"]
                )
            else:
                normalized_roles.append(
                    row["title"]
                )

            if (index + 1) % 25 == 0:

                print(
                    f"Processed {index + 1}/{len(df)} jobs..."
                )

        # Add new columns
        df["normalized_technical_skills"] = normalized_rows
        df["normalized_role"] = normalized_roles

        # --------------------------------------------
        # Create output folder
        # --------------------------------------------

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------
        # Save CSV
        # --------------------------------------------

        df.to_csv(
            NORMALIZED_JOBS,
            index=False
        )

        print()
        print("=" * 60)
        print("NORMALIZED JOBS SAVED")
        print("=" * 60)
        print(NORMALIZED_JOBS)

        return df


if __name__ == "__main__":

    pipeline = NormalizationPipeline()

    df = pipeline.load_dataset()

    print()
    print("=" * 60)
    print("SAMPLE SKILL COLUMNS")
    print("=" * 60)

    columns = [
        "technical_skills",
        "soft_skills",
        "tools",
        "certifications",
        "experience",
        "education"
    ]

    for column in columns:

        print()
        print(column)
        print("-" * 50)
        print(df.iloc[0][column])

    skills = [

        "Python",

        "Pyhton",

        "Power BI",

        "Tensor Flow",

        "Business Analytics",

        "Machine Learnng",

        "SQL",

        "Artificial Intelligence",

        "Snowflake",

        "Tableau"

    ]

    print()
    print("=" * 60)
    print("NORMALIZING DATASET")
    print("=" * 60)

    df = pipeline.process_dataset(df)

    print()
    print(df[["job_id", "normalized_technical_skills"]].head())