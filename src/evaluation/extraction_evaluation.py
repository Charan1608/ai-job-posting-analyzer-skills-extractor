"""
=========================================================
EXTRACTION EVALUATION
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
import pandas as pd

from src.normalization.config import PROJECT_ROOT


# --------------------------------------------------------
# File Paths
# --------------------------------------------------------

GROUND_TRUTH_FILE = (
    PROJECT_ROOT
    / "ground_truth_review_final200(3).csv"
)

AI_OUTPUT_FILE = (
    PROJECT_ROOT
    / "sample_200_with_ai_skills(3).csv"
)

OUTPUT_FOLDER = (
    PROJECT_ROOT
    / "outputs"
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)
# --------------------------------------------------------
# Evaluation Class
# --------------------------------------------------------

class ExtractionEvaluation:

    def __init__(self):

        print("=" * 60)
        print("EXTRACTION EVALUATION")
        print("=" * 60)

        self.ground_truth = pd.read_csv(
            GROUND_TRUTH_FILE
        )

        self.ai_output = pd.read_csv(
            AI_OUTPUT_FILE
        )

        print()

        print(
            f"Ground Truth Rows : {len(self.ground_truth)}"
        )

        print(
            f"AI Output Rows    : {len(self.ai_output)}"
        )
            # --------------------------------------------------------
    # Parse List
    # --------------------------------------------------------

    def parse_list(self, value):

        if pd.isna(value):

            return set()

        try:

            parsed = ast.literal_eval(value)

            if isinstance(parsed, list):

                cleaned = {

                    str(x).strip().lower()

                    for x in parsed

                    if str(x).strip()

                }

                return cleaned

        except Exception:

            pass

        return set()
    # --------------------------------------------------------
# Main
# --------------------------------------------------------

if __name__ == "__main__":

    evaluator = ExtractionEvaluation()