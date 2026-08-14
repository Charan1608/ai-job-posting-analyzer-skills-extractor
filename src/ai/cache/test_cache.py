"""
=========================================================
CACHE TEST
=========================================================
"""

from src.ai.cache.cache_manager import CacheManager

cache = CacheManager()

job_id = 123456

sample = {
    "technical_skills": [
        "Python",
        "SQL"
    ]
}

existing = cache.get(job_id)

if existing:

    print("Loaded from cache")

    print(existing)

else:

    print("Saving to cache...")

    cache.save(job_id, sample)

    print(cache.get(job_id))