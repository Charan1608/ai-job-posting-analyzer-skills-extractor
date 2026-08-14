"""
=========================================================
EVALUATION METRICS
AI-Powered Job Posting Analyzer
=========================================================
"""

from typing import Set


def precision(tp: int, fp: int) -> float:
    """
    Precision = TP / (TP + FP)
    """
    if tp + fp == 0:
        return 0.0

    return tp / (tp + fp)


def recall(tp: int, fn: int) -> float:
    """
    Recall = TP / (TP + FN)
    """
    if tp + fn == 0:
        return 0.0

    return tp / (tp + fn)


def f1_score(p: float, r: float) -> float:
    """
    Harmonic Mean
    """
    if p + r == 0:
        return 0.0

    return 2 * p * r / (p + r)


def jaccard_similarity(
    predicted: Set[str],
    actual: Set[str]
) -> float:
    """
    Jaccard Similarity
    """

    union = predicted | actual

    if len(union) == 0:
        return 1.0

    return len(predicted & actual) / len(union)


def exact_match(
    predicted: Set[str],
    actual: Set[str]
) -> bool:
    """
    Exact Match
    """

    return predicted == actual


def coverage(
    predicted: Set[str]
) -> float:
    """
    Coverage
    """

    if len(predicted) == 0:
        return 0.0

    return 1.0
def compare_sets(
    predicted: set,
    actual: set
):
    """
    Compare predicted vs actual skills.
    """

    tp = len(predicted & actual)

    fp = len(predicted - actual)

    fn = len(actual - predicted)

    return tp, fp, fn
def calculate_metrics(tp: int, fp: int, fn: int):
    """
    Calculate all evaluation metrics.
    """

    p = precision(tp, fp)
    r = recall(tp, fn)
    f1 = f1_score(p, r)

    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "Precision": p,
        "Recall": r,
        "F1": f1,
    }