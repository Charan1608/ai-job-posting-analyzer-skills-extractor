"""
=========================================================
CACHE MANAGER
=========================================================
"""

from src.ai.cache.cache_utils import (
    cache_exists,
    load_cache,
    save_cache,
)


class CacheManager:

    def get(self, job_id):

        if cache_exists(job_id):
            return load_cache(job_id)

        return None

    def save(self, job_id, result):

        save_cache(job_id, result)