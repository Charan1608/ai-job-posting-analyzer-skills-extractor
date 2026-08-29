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

# Load .env file for local development
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
# Validate API Key
# ---------------------------------------------------------

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Add it to .env locally or configure it in "
        "Streamlit Cloud Secrets."
    )


# ---------------------------------------------------------
# Initialize Groq Client
# ---------------------------------------------------------

client = Groq(api_key=API_KEY)


# ---------------------------------------------------------
# Groq Client
# ---------------------------------------------------------

class GroqClient:

    def __init__(self):
        self.client = client
        self.prompt = load_prompt()

    # -----------------------------------------------------
    # Extract Skills Using Groq LLM
    # -----------------------------------------------------

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2),
        reraise=True
    )
    def extract(self, job_description: str):

        try:

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

            # -------------------------------------------------
            # Read LLM Response
            # -------------------------------------------------

            result = response.choices[0].message.content

            # -------------------------------------------------
            # Convert JSON String to Python Dictionary
            # -------------------------------------------------

            return json.loads(result)

        except Exception as e:

            # -------------------------------------------------
            # Diagnostic Error Information
            # -------------------------------------------------

            print(
                f"GROQ ERROR TYPE: {type(e).__name__}"
            )

            print(
                f"GROQ ERROR: {e}"
            )

            # Re-raise the original exception so that
            # Tenacity/Streamlit can display the real error.
            raise


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
