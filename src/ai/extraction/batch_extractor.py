"""
=========================================================
RESUMABLE BATCH AI EXTRACTION
AI-Powered Job Posting Analyzer
=========================================================
"""

import ast
import json
from pathlib import Path

import pandas as pd

from src.ai.extraction.dataset_loader import load_dataset
from src.ai.extraction.extractor import SkillExtractor
from src.ai.extraction.progress_tracker import show_progress


OUTPUT_FILE = Path("data/processed/sample_200_with_ai_skills.csv")


class BatchExtractor:

    def __init__(self):

        print("=" * 60)
        print("RESUMABLE AI EXTRACTION")
        print("=" * 60)

        self.extractor = SkillExtractor()

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------
    # Count extracted skills
    # ---------------------------------------------------

    @staticmethod
    def skill_count(value):

        try:

            skills = ast.literal_eval(str(value))

            if isinstance(skills, list):
                return len(skills)

        except Exception:
            pass

        return 0

    # ---------------------------------------------------

    def run(self):

        df = load_dataset()

        total_jobs = len(df)

        # ---------------------------------------------------
        # Resume Support
        # ---------------------------------------------------

        if OUTPUT_FILE.exists():

            existing = pd.read_csv(OUTPUT_FILE)

            completed_ids = set()

            for _, r in existing.iterrows():

                total = (
                    self.skill_count(r["technical_skills"])
                    + self.skill_count(r["tools"])
                    + self.skill_count(r["soft_skills"])
                    + self.skill_count(r["certifications"])
                )

                if total > 0:
                    completed_ids.add(r["job_id"])

            results = existing.to_dict("records")

            print("\nResuming previous extraction...")
            print(f"Completed Jobs : {len(completed_ids)}")
            print(f"Pending Jobs   : {total_jobs - len(completed_ids)}")

        else:

            completed_ids = set()
            results = []

            print("\nStarting new extraction...")
              
        

               # ---------------------------------------------------
        # Extraction Loop
        # ---------------------------------------------------

        for _, row in df.iterrows():

            job_id = row["job_id"]

            if job_id in completed_ids:
                continue

            description = str(row["description"])

            try:

                result = self.extractor.extract(

                    job_id=job_id,

                    description=description

                )

                # -----------------------------------------
                # Reject Empty Extraction
                # -----------------------------------------

                total_skills = (

                    len(result["technical_skills"])

                    + len(result["tools"])

                    + len(result["soft_skills"])

                    + len(result["certifications"])

                )

                if total_skills == 0:

                    raise ValueError(

                        f"Empty extraction returned for Job {job_id}"

                    )

            except Exception as e:

                print(f"\nERROR [{job_id}] : {e}")

                continue
            # -----------------------------------------
            # Save Record
            # -----------------------------------------

            record = row.to_dict()

            record["technical_skills"] = json.dumps(
                result["technical_skills"]
            )

            record["tools"] = json.dumps(
                result["tools"]
            )

            record["soft_skills"] = json.dumps(
                result["soft_skills"]
            )

            record["certifications"] = json.dumps(
                result["certifications"]
            )

            record["experience"] = result["experience"]

            record["education"] = result["education"]

            updated = False

            for i, r in enumerate(results):

                if r["job_id"] == job_id:

                    results[i] = record

                    updated = True

                    break

            if not updated:

                results.append(record)

            completed_ids.add(job_id)

            pd.DataFrame(results).to_csv(
                OUTPUT_FILE,
                index=False
            )

            print(f"\nSaved Job : {job_id}")

            print(
                f"Completed : {len(completed_ids)}/{total_jobs}"
            )

            show_progress(
                len(completed_ids),
                total_jobs
            )
            

              # ---------------------------------------------------

        pd.DataFrame(
            results
        ).to_csv(
            OUTPUT_FILE,
            index=False
        )

        print("\n" + "=" * 60)
        print("EXTRACTION COMPLETED")
        print("=" * 60)

        successful = sum(
            1
            for r in results
            if (
                self.skill_count(r["technical_skills"])
                + self.skill_count(r["tools"])
                + self.skill_count(r["soft_skills"])
                + self.skill_count(r["certifications"])
            ) > 0
        )

        print(f"Successful Jobs : {successful}")
        print(f"Pending Jobs    : {total_jobs - successful}")
        print(f"Output          : {OUTPUT_FILE}")


if __name__ == "__main__":

    BatchExtractor().run()