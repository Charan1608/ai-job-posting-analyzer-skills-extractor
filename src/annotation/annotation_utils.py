"""
=========================================================
ANNOTATION UTILITIES
=========================================================
"""

import json
import pandas as pd


def json_to_text(value):

    if pd.isna(value):
        return ""

    try:
        items = json.loads(value)

        if not isinstance(items, list):
            return ""

        cleaned = []

        for item in items:

            if item is None:
                continue

            item = str(item).strip()

            if item != "":
                cleaned.append(item)

        return "\n".join(cleaned)

    except Exception as e:

        return str(value)

    cleaned = []

    for item in items:

        if item is None:
            continue

        item = str(item).strip()

        if item == "":
            continue

        cleaned.append(item)

    return "\n".join(cleaned)


def text_to_json(text):

    skills = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            skills.append(line)

    return json.dumps(skills, ensure_ascii=False)


def reviewed_jobs(df):

    return (
        df["review_status"]
        .fillna("")
        .eq("Reviewed")
        .sum()
    )


def remaining_jobs(df):

    return len(df) - reviewed_jobs(df)


def progress(current, total):

    return current / total