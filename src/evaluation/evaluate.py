"""
=========================================================
RUN SKILL EXTRACTION EVALUATION
=========================================================
"""

from pathlib import Path

from src.evaluation.evaluator import Evaluator
from src.evaluation.reports import (
    save_summary,
    save_per_job,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

JOBS_FILE = PROJECT_ROOT / "data" / "processed" / "normalized_jobs.csv"

AI_FILE = PROJECT_ROOT / "data" / "processed" / "normalized_skills_long.csv"

GROUND_TRUTH_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ground_truth_normalized_skills_long.csv"
)


def main():

    print("=" * 60)
    print("SKILL EXTRACTION EVALUATION")
    print("=" * 60)

    evaluator = Evaluator(
        JOBS_FILE,
        AI_FILE,
        GROUND_TRUTH_FILE
    )

    summary, per_job = evaluator.evaluate()

    save_summary(summary)
    save_per_job(per_job)

    print("\nEvaluation Complete\n")

    print(f"Jobs Evaluated : {summary['jobs']}")

    print()

    print(f"TP : {summary['tp']}")
    print(f"FP : {summary['fp']}")
    print(f"FN : {summary['fn']}")

    print()

    print(f"Precision : {summary['precision']:.4f}")
    print(f"Recall    : {summary['recall']:.4f}")
    print(f"F1 Score  : {summary['f1']:.4f}")
    print(f"Jaccard   : {summary['avg_jaccard']:.4f}")
    print(f"Exact     : {summary['exact_match_rate']:.4f}")

    print("\nReports Saved Successfully")


if __name__ == "__main__":
    main()