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

# Load .env for local development
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")


# =========================================================
# STREAMLIT CLOUD SECRETS
# =========================================================

if not API_KEY:

    try:

        import streamlit as st

        API_KEY = st.secrets.get("GROQ_API_KEY")

    except Exception:

        API_KEY = None


# =========================================================
# API KEY VALIDATION
# =========================================================

if not API_KEY:

    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Add GROQ_API_KEY to Streamlit Cloud Secrets."
    )


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=API_KEY
)


# =========================================================
# GROQ CLIENT CLASS
# =========================================================

class GroqClient:

    def __init__(self):

        self.client = client

        self.prompt = load_prompt()


    # =====================================================
    # EXTRACT JOB INFORMATION
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
    def extract(
        self,
        job_description: str
    ):

        # -------------------------------------------------
        # Validate input
        # -------------------------------------------------

        if not job_description:

            raise ValueError(
                "Job description cannot be empty."
            )


        job_description = job_description.strip()


        if not job_description:

            raise ValueError(
                "Job description cannot be empty."
            )


        # -------------------------------------------------
        # Prevent excessively large requests
        #
        # Groq free/on-demand limits can reject requests
        # when the combined prompt and output exceed TPM.
        # -------------------------------------------------

        MAX_INPUT_CHARACTERS = 16000

        if len(job_description) > MAX_INPUT_CHARACTERS:

            job_description = (
                job_description[
                    :MAX_INPUT_CHARACTERS
                ]
            )


        # =================================================
        # USER PROMPT
        # =================================================

        user_message = (
            "Analyze this job posting and extract the "
            "information required by the system schema.\n\n"
            "Identify explicit technical skills, tools and "
            "technologies, soft skills, certifications, "
            "education requirements and experience "
            "requirements.\n\n"
            "Return ONLY valid JSON.\n\n"
            "JOB POSTING:\n"
            + job_description
        )


        # =================================================
        # GROQ API REQUEST
        # =================================================

        response = self.client.chat.completions.create(

            model=MODEL_NAME,

            # Deterministic extraction
            temperature=0,

            # Reduced from 4096 to stay within TPM limit
            max_tokens=2000,

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
                    "content": user_message
                }

            ]
        )


        # =================================================
        # CHECK RESPONSE
        # =================================================

        if not response.choices:

            raise ValueError(
                "Groq returned no choices."
            )


        message = response.choices[0].message

        result = message.content


        if not result:

            raise ValueError(
                "Groq returned an empty response."
            )


        # =================================================
        # PARSE JSON
        # =================================================

        try:

            data = json.loads(result)

        except json.JSONDecodeError as error:

            raise ValueError(
                "Groq returned invalid JSON."
            ) from error


        # =================================================
        # ENSURE REQUIRED FIELDS
        # =================================================

        data.setdefault(
            "technical_skills",
            []
        )

        data.setdefault(
            "soft_skills",
            []
        )

        data.setdefault(
            "tools",
            []
        )

        data.setdefault(
            "certifications",
            []
        )

        data.setdefault(
            "experience",
            None
        )

        data.setdefault(
            "education",
            None
        )


        # =================================================
        # NORMALIZE LIST FIELDS
        # =================================================

        list_fields = [

            "technical_skills",

            "soft_skills",

            "tools",

            "certifications"

        ]


        for field in list_fields:

            value = data.get(field)


            # None → empty list

            if value is None:

                data[field] = []


            # String → single-item list

            elif isinstance(value, str):

                data[field] = [
                    value
                ]


            # Tuple/set/etc. → list

            elif not isinstance(value, list):

                try:

                    data[field] = list(value)

                except TypeError:

                    data[field] = []


        # =================================================
        # CLEAN LIST VALUES
        # =================================================

        for field in list_fields:

            cleaned = []


            for item in data[field]:

                if item is None:

                    continue


                item = str(item).strip()


                if item:

                    cleaned.append(item)


            data[field] = cleaned


        # =================================================
        # RETURN STRUCTURED RESULT
        # =================================================

        return data


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    We are looking for a Business Analyst with experience
    in Python, SQL, Power BI, Tableau, Microsoft Excel,
    Statistics, Business Analysis, Machine Learning and
    Azure.

    Responsibilities include gathering business
    requirements, performing data analysis, creating
    dashboards and reports, and working with stakeholders.

    Bachelor's degree required.

    3-5 years of experience preferred.

    AWS certification is preferred.

    Strong communication and leadership skills required.

    """


    groq_client = GroqClient()


    output = groq_client.extract(
        sample
    )


    print(
        json.dumps(
            output,
            indent=4
        )
    )