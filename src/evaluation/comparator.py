"""
=========================================================
COMPARATOR
=========================================================
"""


class SkillComparator:

    @staticmethod
    def compare(predicted, actual):

        predicted = set(predicted)
        actual = set(actual)

        tp = predicted & actual

        fp = predicted - actual

        fn = actual - predicted

        return {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tp_count": len(tp),
            "fp_count": len(fp),
            "fn_count": len(fn),
        }