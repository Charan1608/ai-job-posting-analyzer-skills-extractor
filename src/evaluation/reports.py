"""
=========================================================
EVALUATION REPORTS
=========================================================
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_summary(summary):

    df = pd.DataFrame([summary])

    df.to_csv(
        OUTPUT_DIR / "evaluation_summary.csv",
        index=False
    )


def save_per_job(per_job):

    df = pd.DataFrame(per_job)

    df.to_csv(
        OUTPUT_DIR / "evaluation_per_job.csv",
        index=False
    )