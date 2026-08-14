"""
=========================================================
CACHE UTILITIES
=========================================================
"""

import json
from pathlib import Path

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_file(job_id):
    return CACHE_DIR / f"{job_id}.json"


def cache_exists(job_id):
    return cache_file(job_id).exists()


def load_cache(job_id):

    with open(cache_file(job_id), "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(job_id, data):

    with open(cache_file(job_id), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)