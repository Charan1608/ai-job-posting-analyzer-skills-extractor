"""
=========================================================
FEATURE ENGINEERING V2
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast

import joblib
import pandas as pd

from src.normalization.config import PROJECT_ROOT


# --------------------------------------------------------
# File Paths
# --------------------------------------------------------

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "feature_engineered_jobs_v2.csv"
)

MODEL_FOLDER = PROJECT_ROOT / "models"

TECHNOLOGY_VOCAB_FILE = MODEL_FOLDER / "technology_vocabulary.pkl"


# --------------------------------------------------------
# Shared category list (training bulk features + single-job
# inference features both build from this exact same list,
# so there is only ever one place that defines it).
# --------------------------------------------------------

CATEGORIES = [

    "Programming Language",
    "Database",
    "Database Language",
    "BI Tool",
    "Cloud",
    "Cloud Data Warehouse",
    "Machine Learning",
    "Artificial Intelligence",
    "Big Data",
    "Data Engineering",
    "DevOps",
    "Version Control",
    "ETL",
    "Spreadsheet",
    "Analytics",
    "Business Analysis"

]


class FeatureEngineeringV2:

    # --------------------------------------------------------
    # Initialize
    # --------------------------------------------------------

    def __init__(self, load_data=True):

        print("=" * 60)
        print("FEATURE ENGINEERING V2")
        print("=" * 60)

        # `load_data=False` is used by inference code (JobRolePredictor),
        # which only needs the feature-building logic below and never
        # reads the training CSV. Training callers are unaffected: the
        # default remains True, so `FeatureEngineeringV2()` behaves
        # exactly as before.
        self.df = None
        self.skills = []
        self.technologies = []
        self.binary_features = None
        self.category_features = None
        self.final_df = None

        if load_data:

            self.df = pd.read_csv(INPUT_FILE)

            print(f"Rows Loaded : {len(self.df):,}")

        else:

            print("Data Loading Skipped : running in inference mode")

    # --------------------------------------------------------
    # Parse Normalized Skills
    # --------------------------------------------------------

    def parse_skills(self):

        print()
        print("=" * 60)
        print("PARSING NORMALIZED SKILLS")
        print("=" * 60)

        parsed = []

        for value in self.df["normalized_technical_skills"]:

            if pd.isna(value):

                parsed.append([])
                continue

            try:
                parsed.append(ast.literal_eval(value))

            except Exception:
                parsed.append([])

        self.skills = parsed

        print(f"Jobs Parsed : {len(self.skills):,}")

        if self.skills:

            print()
            print("First Job Skills")
            print("-" * 60)

            for skill in self.skills[0][:5]:
                print(skill)

       # --------------------------------------------------------
    # Build Technology Vocabulary Automatically
    # --------------------------------------------------------

    def build_technology_list(self):

        print()
        print("=" * 60)
        print("BUILDING TECHNOLOGY VOCABULARY")
        print("=" * 60)

        skill_counts = {}

        for job in self.skills:

            for skill in job:

                name = str(
                    skill.get("normalized", "")
                ).strip()

                if not name:
                    continue

                category = str(
                    skill.get("skill_type", "")
                ).lower()

                # Keep only technical skills
                allowed_categories = {

                    "programming language",
                    "database",
                    "database language",
                    "bi tool",
                    "cloud",
                    "cloud data warehouse",
                    "machine learning",
                    "artificial intelligence",
                    "big data",
                    "data engineering",
                    "devops",
                    "version control",
                    "etl",
                    "spreadsheet",
                    "python library"

                }

                if category not in allowed_categories:
                    continue

                skill_counts[name] = (
                    skill_counts.get(name, 0) + 1
                )

        skill_counts = dict(

            sorted(
                skill_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )

        )

        self.technologies = list(skill_counts.keys())[:75]

        print(
            f"Technology Features : {len(self.technologies)}"
        )

        print()

        print("Top Technologies")

        print("-" * 60)

        for tech in self.technologies[:20]:

            print(tech)

        # ----------------------------------------------------
        # Persist the vocabulary. This is what guarantees
        # inference builds the exact same 75 "has_*" columns,
        # in the exact same order, as training -- instead of
        # JobRolePredictor recreating (and silently drifting
        # from) its own copy of this list.
        # ----------------------------------------------------

        MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.technologies, TECHNOLOGY_VOCAB_FILE)

        print()
        print(f"Saved Technology Vocabulary : {TECHNOLOGY_VOCAB_FILE}")

    # --------------------------------------------------------
    # Per-Job Feature Builders (single source of truth)
    #
    # These two helpers contain the ONLY implementation of
    # "how do we turn one job's normalized skills into binary
    # technology features / category features". Both the bulk
    # training methods below (create_binary_features,
    # create_category_features) and the single-job inference
    # method (build_single_feature_vector) call these same
    # helpers, so training and inference can never diverge.
    # --------------------------------------------------------

    def _binary_features_for_job(self, job):

        row = {}

        for tech in self.technologies:

            column = (
                "has_"
                + tech.lower()
                .replace(" ", "_")
                .replace("+", "plus")
            )

            row[column] = 0

        for skill in job:

            normalized = str(
                skill.get("normalized", "")
            ).strip().lower()

            for tech in self.technologies:

                if (
                    normalized == tech.lower()
                    or tech.lower() in normalized
                    or normalized in tech.lower()
                ):

                    column = (
                        "has_"
                        + tech.lower()
                        .replace(" ", "_")
                        .replace("+", "plus")
                    )

                    row[column] = 1

        return row

    def _category_features_for_job(self, job):

        counts = {category: 0 for category in CATEGORIES}

        for skill in job:

            category = str(
                skill.get("skill_type", "")
            ).strip()

            if category in counts:

                counts[category] += 1

        row = {

            "total_skills": len(job),

            "programming_languages":
                counts["Programming Language"],

            "databases":
                counts["Database"] +
                counts["Database Language"],

            "bi_tools":
                counts["BI Tool"],

            "cloud_tools":
                counts["Cloud"] +
                counts["Cloud Data Warehouse"],

            "ml_skills":
                counts["Machine Learning"],

            "ai_skills":
                counts["Artificial Intelligence"],

            "big_data":
                counts["Big Data"],

            "data_engineering":
                counts["Data Engineering"],

            "devops":
                counts["DevOps"],

            "version_control":
                counts["Version Control"],

            "etl_tools":
                counts["ETL"],

            "spreadsheet":
                counts["Spreadsheet"],

            "analytics":
                counts["Analytics"],

            "business_analysis":
                counts["Business Analysis"],

            "skill_diversity":

                sum(
                    1
                    for value in counts.values()
                    if value > 0
                )
        }

        return row

    @staticmethod
    def _apply_composite_scores(row):
        """
        Add composite score fields to `row` in place and return it.

        Works identically whether `row` is a plain dict for a single
        job (values are ints -> scalar arithmetic) or the bulk
        `category_features` DataFrame (values are columns -> Series
        arithmetic), because `+` behaves the same way in both cases.
        This is what keeps the composite-score formulas defined in
        exactly one place for both training and inference.
        """

        row["analytics_score"] = (

            row["analytics"]

            + row["business_analysis"]

            + row["bi_tools"]

        )

        row["data_engineering_score"] = (

            row["data_engineering"]

            + row["big_data"]

            + row["databases"]

        )

        row["ai_readiness_score"] = (

            row["ai_skills"]

            + row["ml_skills"]

            + row["programming_languages"]

        )

        row["cloud_score"] = (

            row["cloud_tools"]

            + row["devops"]

        )

        row["visualization_score"] = (

            row["bi_tools"]

            + row["spreadsheet"]

        )

        return row

    # --------------------------------------------------------
    # Create Binary Technology Features
    # --------------------------------------------------------

    def create_binary_features(self):

        print()
        print("=" * 60)
        print("CREATING BINARY TECHNOLOGY FEATURES")
        print("=" * 60)

        rows = [
            self._binary_features_for_job(job)
            for job in self.skills
        ]

        self.binary_features = pd.DataFrame(rows)

        print(
            f"Binary Feature Columns : {self.binary_features.shape[1]}"
        )

        print()
        print(self.binary_features.head())

    # --------------------------------------------------------
    # Create Category Features
    # --------------------------------------------------------

    def create_category_features(self):

        print()
        print("=" * 60)
        print("CREATING CATEGORY FEATURES")
        print("=" * 60)

        rows = [
            self._category_features_for_job(job)
            for job in self.skills
        ]

        self.category_features = pd.DataFrame(rows)

        print(
            f"Category Features : {self.category_features.shape[1]}"
        )

        print()

        print(self.category_features.head())

    # --------------------------------------------------------
    # Create Composite Scores
    # --------------------------------------------------------

    def create_composite_scores(self):

        print()
        print("=" * 60)
        print("CREATING COMPOSITE SCORES")
        print("=" * 60)

        self.category_features = self._apply_composite_scores(
            self.category_features
        )

        print()

        print(self.category_features.head())

    # --------------------------------------------------------
    # Build Single-Job Feature Vector (for inference)
    # --------------------------------------------------------

    def build_single_feature_vector(self, normalized_skills):
        """
        Build the raw feature vector for ONE job's normalized technical
        skills, using exactly the same logic (via the shared helpers
        above) as the bulk training pipeline:

            create_binary_features + create_category_features
            + create_composite_scores

        Column order matches training exactly: category/composite
        features first, then the "has_*" technology columns -- the
        same order produced by save_feature_dataset's
        pd.concat([base, category_features, binary_features], axis=1).

        Requires `self.technologies` to be populated first, either by
        calling build_technology_list() (training) or by assigning a
        saved vocabulary loaded via joblib (inference).

        Returns a single-row pandas DataFrame.
        """

        if not self.technologies:
            raise ValueError(
                "Technology vocabulary is empty. Call "
                "build_technology_list() or assign a saved vocabulary "
                "to `self.technologies` before calling "
                "build_single_feature_vector()."
            )

        category_row = self._category_features_for_job(normalized_skills)

        category_row = self._apply_composite_scores(category_row)

        binary_row = self._binary_features_for_job(normalized_skills)

        combined_row = {**category_row, **binary_row}

        return pd.DataFrame([combined_row])

    # --------------------------------------------------------
    # Save Feature Dataset
    # --------------------------------------------------------

    def save_feature_dataset(self):

        print()
        print("=" * 60)
        print("SAVING FEATURE DATASET")
        print("=" * 60)

        base_columns = [
            "job_id",
            "company_name",
            "title",
            "location",
            "experience",
            "education",
            "work_type"
        ]

        base = self.df[base_columns].copy()

        final_df = pd.concat(
            [
                base,
                self.category_features,
                self.binary_features
            ],
            axis=1
        )

        final_df.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(f"Rows : {len(final_df):,}")
        print(f"Columns : {final_df.shape[1]}")
        print()
        print(f"Saved to:\n{OUTPUT_FILE}")

        self.final_df = final_df


# --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    feature = FeatureEngineeringV2()

    feature.parse_skills()

    feature.build_technology_list()

    feature.create_binary_features()

    feature.create_category_features()

    feature.create_composite_scores()

    feature.save_feature_dataset()