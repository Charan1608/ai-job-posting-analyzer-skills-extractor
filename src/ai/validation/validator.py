"""
=========================================================
VALIDATOR
AI-Powered Job Posting Analyzer
=========================================================
"""

from src.ai.validation.schema import SkillExtraction


def validate_output(response: dict):

    validated = SkillExtraction(**response)

    return validated.model_dump()


if __name__ == "__main__":

    sample = {
        "technical_skills": ["Python", "SQL"],
        "soft_skills": ["Communication"],
        "tools": ["Power BI"],
        "certifications": ["AWS"],
        "experience": "3-5",
        "education": "Bachelor's"
    }

    print(validate_output(sample))