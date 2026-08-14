"""
=========================================================
TEST EXTRACTION
=========================================================
"""

from src.ai.extraction.extractor import AIExtractor

description = """
Business Analyst

Requirements

Python

SQL

Power BI

Excel

Communication

Bachelor's degree

3 years experience

AWS Certification
"""

extractor = AIExtractor()

result = extractor.extract(
    job_id=999999,
    description=description
)

print("\nFINAL RESULT\n")

print(result)