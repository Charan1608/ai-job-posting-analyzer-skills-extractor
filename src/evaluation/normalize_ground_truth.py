"""
=========================================================
NORMALIZE GROUND TRUTH
AI-Powered Job Posting Analyzer
=========================================================
"""

import json
import ast
from pathlib import Path

import pandas as pd

from src.normalization.pipeline import NormalizationPipeline


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "labelled"
    / "ground_truth_review_final200.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ground_truth_normalized_skills_long.csv"
)


def parse_json(value):

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


def normalize_list(
    pipeline,
    job_id,
    skill_type,
    skills,
    rows,
):

    for skill in skills:

        result = pipeline.normalize(skill)

        rows.append({

            "job_id": job_id,

            "skill_type": skill_type,

            "original_skill": skill,

            "normalized_skill": result.get("normalized"),

            "category": result.get("category"),

            "method": result.get("method"),

            "confidence": result.get("confidence"),

            "esco_uri": result.get("esco_uri")

        })


def main():

    print("=" * 60)
    print("NORMALIZING GROUND TRUTH")
    print("=" * 60)

    pipeline = NormalizationPipeline()

    df = pd.read_csv(INPUT_FILE)

    output_rows = []

    for index, row in df.iterrows():

        job_id = row.get("job_id", row.get("ali"))

        print(f"[{index+1}/{len(df)}] {job_id}")

        technical = parse_json(
            row.get("reviewed_technical_skills", [])
        )

        tools = parse_json(
            row.get("reviewed_tools", [])
        )

        soft = parse_json(
            row.get("reviewed_soft_skills", [])
        )

        certifications = parse_json(
            row.get("reviewed_certifications", [])
        )

        normalize_list(
            pipeline,
            job_id,
            "technical",
            technical,
            output_rows
        )

        normalize_list(
            pipeline,
            job_id,
            "tool",
            tools,
            output_rows
        )

        normalize_list(
            pipeline,
            job_id,
            "soft",
            soft,
            output_rows
        )

        normalize_list(
            pipeline,
            job_id,
            "certification",
            certifications,
            output_rows
        )

    output = pd.DataFrame(output_rows)

    output.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("GROUND TRUTH NORMALIZATION COMPLETE")
    print("=" * 60)
    print(f"Rows : {len(output)}")
    print(f"Saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()