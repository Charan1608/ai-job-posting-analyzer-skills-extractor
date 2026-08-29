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


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GROQ_API_KEY")


# ---------------------------------------------------------
# Streamlit Cloud Secrets Fallback
# ---------------------------------------------------------

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets.get("GROQ_API_KEY")
    except Exception:
        API_KEY = None


# ---------------------------------------------------------
# Initialize Groq Client
# ---------------------------------------------------------

client = None

if API_KEY:
    client = Groq(api_key=API_KEY)


# ---------------------------------------------------------
# Groq Client
# ---------------------------------------------------------

class GroqClient:

    def __init__(self):
        self.client = client
        self.prompt = load_prompt()

    # -----------------------------------------------------
    # AI Extraction
    # -----------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2),
        reraise=True
    )
    def extract_with_groq(self, job_description: str):

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
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
                    "content": job_description
                }
            ]
        )

        result = response.choices[0].message.content

        return json.loads(result)

    # -----------------------------------------------------
    # Public Extraction Method
    # -----------------------------------------------------

    def extract(self, job_description: str):

        try:

            if not self.client:
                raise ValueError(
                    "Groq API client is not configured."
                )

            return self.extract_with_groq(job_description)

        except Exception as e:

            print(
                f"GROQ ERROR TYPE: {type(e).__name__}"
            )

            print(
                f"GROQ ERROR: {e}"
            )

            # -------------------------------------------------
            # Demonstration fallback
            # -------------------------------------------------

            return self.fallback_extraction(job_description)

    # -----------------------------------------------------
    # Fallback Skill Extraction
    # -----------------------------------------------------

    def fallback_extraction(self, job_description: str):

        text = job_description.lower()

        skill_dictionary = {

            "Python": ["python"],
            "SQL": ["sql"],
            "Excel": ["excel", "microsoft excel"],
            "Power BI": ["power bi", "powerbi"],
            "Tableau": ["tableau"],
            "R": [" r ", "r programming"],
            "Java": ["java"],
            "AWS": ["aws", "amazon web services"],
            "Azure": ["azure"],
            "GCP": ["gcp", "google cloud"],
            "Machine Learning": [
                "machine learning",
                "machine-learning"
            ],
            "Artificial Intelligence": [
                "artificial intelligence",
                " ai "
            ],
            "Statistics": [
                "statistics",
                "statistical analysis"
            ],
            "Data Analysis": [
                "data analysis",
                "data analytics"
            ],
            "Data Visualization": [
                "data visualization",
                "data visualisation"
            ],
            "Business Intelligence": [
                "business intelligence"
            ],
            "Pandas": ["pandas"],
            "NumPy": ["numpy"],
            "PySpark": ["pyspark"],
            "Spark": ["spark"],
            "Hadoop": ["hadoop"],
            "NLP": [
                "natural language processing",
                "nlp"
            ]
        }

        detected_skills = []

        for skill, keywords in skill_dictionary.items():

            for keyword in keywords:

                if keyword in text:

                    detected_skills.append(skill)

                    break

        # -----------------------------------------------------
        # Basic Role Detection
        # -----------------------------------------------------

        if "data scientist" in text:
            predicted_role = "Data Scientist"

        elif "data engineer" in text:
            predicted_role = "Data Engineer"

        elif "business analyst" in text:
            predicted_role = "Business Analyst"

        elif "data analyst" in text:
            predicted_role = "Data Analyst"

        else:
            predicted_role = "Business Analyst"

        return {
            "skills": detected_skills,
            "predicted_role": predicted_role,
            "source": "Fallback extraction"
        }


# ---------------------------------------------------------
# Local Test
# ---------------------------------------------------------

if __name__ == "__main__":

    sample = """
    Looking for a Business Analyst with Python, SQL,
    Power BI, Tableau, Excel and Azure experience.

    Bachelor's degree required.

    3-5 years experience.

    AWS certification preferred.

    Strong communication and leadership skills.
    """

    groq_client = GroqClient()

    output = groq_client.extract(sample)

    print(
        json.dumps(
            output,
            indent=4
        )
    )
