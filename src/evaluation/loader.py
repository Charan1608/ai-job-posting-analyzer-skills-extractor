"""
=========================================================
EVALUATION LOADER V3
Merge all skill categories into one skill set per job
=========================================================
"""

import pandas as pd


class EvaluationLoader:

    def __init__(self, jobs_file, ai_file, gt_file):

        self.jobs_file = jobs_file
        self.ai_file = ai_file
        self.gt_file = gt_file

    # -------------------------------------------------

    def load_jobs(self):

        jobs = pd.read_csv(self.jobs_file)

        return (
            jobs["job_id"]
            .astype(str)
            .tolist()
        )

    # -------------------------------------------------

    @staticmethod
    def build_lookup(df):

        lookup = {}

        for job_id, group in df.groupby("job_id"):

            skills = set(

                group["normalized_skill"]

                .dropna()

                .astype(str)

                .str.strip()

            )

            lookup[str(job_id)] = skills

        return lookup

    # -------------------------------------------------

    def load_ai(self):

        return self.build_lookup(
            pd.read_csv(self.ai_file)
        )

    # -------------------------------------------------

    def load_ground_truth(self):

        return self.build_lookup(
            pd.read_csv(self.gt_file)
        )