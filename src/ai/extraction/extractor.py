"""
=========================================================
SKILL EXTRACTOR
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.ai.clients.groq_client import GroqClient
from src.ai.validation.validator import validate_output
from src.ai.cache.cache_manager import CacheManager


class SkillExtractor:

    def __init__(self):

        self.client = GroqClient()

        self.cache = CacheManager()

    def extract(self, job_id, description):

        # -------------------------
        # Cache
        # -------------------------

        cached = self.cache.get(job_id)

        if cached is not None:

            print(f"[CACHE] {job_id}")

            return cached

        # -------------------------
        # API
        # -------------------------

        print(f"[API] {job_id}")

        result = self.client.extract(description)

        result = validate_output(result)

        self.cache.save(job_id, result)

        return result


if __name__ == "__main__":

    extractor = SkillExtractor()

    sample = """
    Looking for a Business Analyst with Python,
    SQL, Power BI, Tableau and Azure.

    Bachelor's degree.

    3 years experience.

    AWS certification.

    Communication skills.
    """

    output = extractor.extract(

        job_id="999999",

        description=sample

    )

    print()

    print(output)