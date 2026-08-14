"""
=========================================================
EVALUATION UTILITIES
=========================================================
"""

import ast
import json

import pandas as pd


def parse_list(value):
    """
    Safely convert CSV string to Python list.
    """

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return value

    if not isinstance(value, str):
        return []

    value = value.strip()

    if value == "":
        return []

    try:
        return json.loads(value)

    except Exception:

        try:
            return ast.literal_eval(value)

        except Exception:
            return []


def clean_set(values):
    """
    Convert list to lowercase unique set.
    """

    cleaned = set()

    for value in values:

        if value is None:
            continue

        value = str(value).strip().lower()

        if value == "":
            continue

        cleaned.add(value)

    return cleaned