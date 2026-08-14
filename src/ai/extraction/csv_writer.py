"""
=========================================================
CSV WRITER
=========================================================
"""

from pathlib import Path
import pandas as pd

OUTPUT = Path("data/processed/ai_extracted_skills.csv")


def save_results(results):

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)

    df.to_csv(
        OUTPUT,
        index=False,
        encoding="utf-8"
    )


def append_result(result):

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame([result])

    if OUTPUT.exists():

        df.to_csv(
            OUTPUT,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8"
        )

    else:

        df.to_csv(
            OUTPUT,
            index=False,
            encoding="utf-8"
        )