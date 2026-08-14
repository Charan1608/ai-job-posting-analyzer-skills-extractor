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

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=API_KEY)

# ---------------------------------------------------------
# Groq Client
# ---------------------------------------------------------


class GroqClient:

    def __init__(self):
        self.client = client
        self.prompt = load_prompt()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2)
    )
    def extract(self, job_description: str):

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},
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


# ---------------------------------------------------------
# Test
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

    client = GroqClient()

    output = client.extract(sample)

    print(json.dumps(output, indent=4))