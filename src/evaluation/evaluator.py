"""
=========================================================
EVALUATOR V3
Skill Extraction Evaluation
=========================================================
"""

from src.evaluation.loader import EvaluationLoader
from src.evaluation.comparator import SkillComparator
from src.evaluation.metrics import (
    precision,
    recall,
    f1_score,
    jaccard_similarity,
    exact_match,
)


class Evaluator:

    def __init__(
        self,
        jobs_file,
        ai_file,
        gt_file
    ):

        self.loader = EvaluationLoader(
            jobs_file,
            ai_file,
            gt_file
        )

    def evaluate(self):

        jobs = self.loader.load_jobs()

        ai = self.loader.load_ai()

        gt = self.loader.load_ground_truth()

        print("=" * 60)
        print("SKILL EXTRACTION EVALUATION")
        print("=" * 60)

        print(f"Jobs Evaluated : {len(jobs)}")

        total_tp = 0
        total_fp = 0
        total_fn = 0

        total_jaccard = 0
        exact_matches = 0

        per_job = []

        for job_id in jobs:

            predicted = ai.get(job_id, set())

            actual = gt.get(job_id, set())

            result = SkillComparator.compare(
                predicted,
                actual
            )

            tp = result["tp_count"]
            fp = result["fp_count"]
            fn = result["fn_count"]

            p = precision(tp, fp)
            r = recall(tp, fn)
            f1 = f1_score(p, r)

            jac = jaccard_similarity(
                predicted,
                actual
            )

            em = exact_match(
                predicted,
                actual
            )

            total_tp += tp
            total_fp += fp
            total_fn += fn

            total_jaccard += jac

            if em:
                exact_matches += 1

            per_job.append({

                "job_id": job_id,

                "predicted_count": len(predicted),

                "actual_count": len(actual),

                "tp": tp,

                "fp": fp,

                "fn": fn,

                "precision": p,

                "recall": r,

                "f1": f1,

                "jaccard": jac,

                "exact_match": em,

                "predicted":
                    ", ".join(sorted(predicted)),

                "actual":
                    ", ".join(sorted(actual)),

                "false_positive_skills":
                    ", ".join(sorted(result["fp"])),

                "false_negative_skills":
                    ", ".join(sorted(result["fn"]))
            })

        overall_precision = precision(
            total_tp,
            total_fp
        )

        overall_recall = recall(
            total_tp,
            total_fn
        )

        overall_f1 = f1_score(
            overall_precision,
            overall_recall
        )

        summary = {

            "jobs": len(jobs),

            "tp": total_tp,

            "fp": total_fp,

            "fn": total_fn,

            "precision": overall_precision,

            "recall": overall_recall,

            "f1": overall_f1,

            "avg_jaccard":
                total_jaccard / len(jobs),

            "exact_match_rate":
                exact_matches / len(jobs)

        }

        return summary, per_job