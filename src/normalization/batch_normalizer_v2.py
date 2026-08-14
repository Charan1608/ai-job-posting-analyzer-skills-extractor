"""
=========================================================
PROFESSIONAL BATCH NORMALIZER V2
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
import json
from typing import List

import pandas as pd

from src.normalization.pipeline import NormalizationPipeline
from src.normalization.config import INPUT_FILE

from src.normalization.exporters import (
    save_jobs,
    save_long_table,
    save_summary,
    save_quality,
    save_unmatched,
)

from src.normalization.statistics import (
    method_statistics,
    category_statistics,
    skill_type_statistics,
    top_skills,
    confidence_statistics,
)

from src.normalization.quality_report import (
    build_quality_report,
)


class BatchNormalizerV2:
    """
    Professional Batch Skill Normalizer
    """

    def __init__(
        self,
        input_file=INPUT_FILE,
        reviewed=False
    ):

        print("=" * 60)
        print("PROFESSIONAL BATCH NORMALIZER V2")
        print("=" * 60)

        self.pipeline = NormalizationPipeline()

        self.input_file = input_file

        self.reviewed = reviewed

        self.jobs_output = []

        self.long_output = []

        self.unmatched = []

    # -----------------------------------------------------
    # Safe JSON Parser
    # -----------------------------------------------------

    @staticmethod
    def parse_json(value) -> List[str]:

        if pd.isna(value):
            return []

        if isinstance(value, list):
            return value

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                return []

            try:
                return json.loads(value)

            except Exception:

                try:
                    return ast.literal_eval(value)

                except Exception:
                    return [value]

        return []
        # -----------------------------------------------------
    # Normalize List of Skills
    # -----------------------------------------------------

    def normalize_list(
        self,
        job_id,
        skill_type,
        skills
    ):

        normalized_names = []

        for skill in skills:

            result = self.pipeline.normalize(skill)

            normalized_names.append(
                result.get("normalized")
            )

            row = {
                "job_id": job_id,
                "skill_type": skill_type,
                "original_skill": skill,
                "normalized_skill": result.get("normalized"),
                "category": result.get("category"),
                "method": result.get("method"),
                "confidence": result.get("confidence"),
                "esco_uri": result.get("esco_uri"),
            }

            self.long_output.append(row)

            if result.get("method") == "unmatched":
                self.unmatched.append(skill)

        return normalized_names
        # -----------------------------------------------------
    # Main Runner
    # -----------------------------------------------------

    def run(self):

        print("\nLoading dataset...")

        df = pd.read_csv(self.input_file)

        print(f"Rows : {len(df)}")

        for index, row in df.iterrows():

            job_id = row["job_id"]

            print(
                f"[{index + 1}/{len(df)}] Processing {job_id}"
            )

            # ---------------------------------------------
            # Ground Truth Review Sheet
            # ---------------------------------------------

            if self.reviewed:

                technical = self.parse_json(
                    row.get("reviewed_technical_skills", [])
                )

                tools = self.parse_json(
                    row.get("reviewed_tools", [])
                )

                soft = self.parse_json(
                    row.get("reviewed_soft_skills", [])
                )

                certifications = self.parse_json(
                    row.get("reviewed_certifications", [])
                )

            # ---------------------------------------------
            # AI Extraction Dataset
            # ---------------------------------------------

            else:

                technical = self.parse_json(
                    row.get("technical_skills", [])
                )

                tools = self.parse_json(
                    row.get("tools", [])
                )

                soft = self.parse_json(
                    row.get("soft_skills", [])
                )

                certifications = self.parse_json(
                    row.get("certifications", [])
                )

            # ---------------------------------------------
            # Normalize Skills
            # ---------------------------------------------

            tech_norm = self.normalize_list(
                job_id,
                "technical",
                technical
            )

            tool_norm = self.normalize_list(
                job_id,
                "tool",
                tools
            )

            soft_norm = self.normalize_list(
                job_id,
                "soft",
                soft
            )

            cert_norm = self.normalize_list(
                job_id,
                "certification",
                certifications
            )
            self.jobs_output.append({

                "job_id": job_id,

                "title": row.get("title"),

                "company_name": row.get("company_name"),

                "technical_skills": json.dumps(tech_norm),

                "tools": json.dumps(tool_norm),

                "soft_skills": json.dumps(soft_norm),

                "certifications": json.dumps(cert_norm),

                "experience": row.get("experience"),

                "education": row.get("education")

            })
                    # --------------------------------------------------
        # EXPORT NORMALIZED DATA
        # --------------------------------------------------

        jobs_df = pd.DataFrame(self.jobs_output)
        long_df = pd.DataFrame(self.long_output)

        save_jobs(jobs_df)
        save_long_table(long_df)

        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        summary_df = method_statistics(long_df)

        save_summary(summary_df)

        # --------------------------------------------------
        # QUALITY REPORT
        # --------------------------------------------------

        quality_df = build_quality_report(long_df)

        save_quality(quality_df)

        # --------------------------------------------------
        # UNMATCHED
        # --------------------------------------------------

        unmatched_df = pd.DataFrame(
            {
                "unmatched_skill": self.unmatched
            }
        )

        save_unmatched(unmatched_df)

        print("\nNormalization finished.")

        print("\nNormalization finished.")


if __name__ == "__main__":
    BatchNormalizerV2().run()