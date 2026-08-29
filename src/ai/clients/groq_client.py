"""
=========================================================
GROQ CLIENT
AI-Powered Job Posting Analyzer
=========================================================
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS
from src.ai.prompts.prompt_loader import load_prompt


# =========================================================
# ENVIRONMENT
# =========================================================

ROOT = Path(__file__).resolve().parents[3]

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")


# Streamlit Cloud Secrets
if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets.get("GROQ_API_KEY")
    except Exception:
        API_KEY = None


if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Add GROQ_API_KEY to Streamlit Cloud Secrets."
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(api_key=API_KEY)


class GroqClient:

    def __init__(self):

        self.client = client
        self.prompt = load_prompt()

    # =====================================================
    # EXTRACT
    # =====================================================

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8
        ),
        reraise=True
    )
    def extract(self, job_description: str):

        if not job_description or not job_description.strip():
            raise ValueError(
                "Job description cannot be empty."
            )

        response = self.client.chat.completions.create(

            model=MODEL_NAME,

            temperature=0,

            max_tokens=MAX_TOKENS,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": self.prompt
                },

                {
                    "role": "user",
                    "content": (
                        "Analyze the following job posting and "
                        "extract EVERY explicit professional skill, "
                        "technology, tool, certification, education "
                        "and experience requirement.\n\n"
                        "Return ONLY valid JSON following the "
                        "required schema.\n\n"
                        "JOB POSTING:\n"
                        + job_description
                    )
                }

            ]
        )

        # =================================================
        # READ RESPONSE
        # =================================================

        if not response.choices:
            raise ValueError(
                "Groq returned no choices."
            )

        result = response.choices[0].message.content

        if not result:
            raise ValueError(
                "Groq returned an empty response."
            )

        # =================================================
        # PARSE JSON
        # =================================================

        try:

            data = json.loads(result)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Groq returned invalid JSON: {result}"
            ) from e

        # =================================================
        # ENSURE REQUIRED KEYS
        # =================================================

        data.setdefault("technical_skills", [])
        data.setdefault("soft_skills", [])
        data.setdefault("tools", [])
        data.setdefault("certifications", [])
        data.setdefault("experience", None)
        data.setdefault("education", None)

        # =================================================
        # NORMALIZE TYPES
        # =================================================

        for key in [
            "technical_skills",
            "soft_skills",
            "tools",
            "certifications"
        ]:

            value = data.get(key)

            if value is None:
                data[key] = []

            elif isinstance(value, str):
                data[key] = [value]

            elif not isinstance(value, list):
                data[key] = list(value)

        # =================================================
        # REMOVE EMPTY VALUES
        # =================================================

        for key in [
            "technical_skills",
            "soft_skills",
            "tools",
            "certifications"
        ]:

            data[key] = [
                str(item).strip()
                for item in data[key]
                if str(item).strip()
            ]

        return data


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    We are looking for a Business Analyst with experience in
    Python, SQL, Power BI, Tableau, Microsoft Excel,
    Statistics, Business Analysis, Machine Learning and Azure.

    Responsibilities include gathering business requirements,
    performing data analysis, creating dashboards and reports,
    and working with stakeholders.

    Bachelor's degree required.
    3-5 years of experience preferred.
    AWS certification is preferred.
    Strong communication and leadership skills required.
    """

    groq_client = GroqClient()

    output = groq_client.extract(sample)

    print(
        json.dumps(
            output,
            indent=4
        )
    )
