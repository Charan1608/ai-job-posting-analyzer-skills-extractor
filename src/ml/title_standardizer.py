"""
=========================================================
JOB TITLE STANDARDIZER
AI-Powered Job Posting Analyzer
=========================================================
"""


def standardize_title(title):
    """
    Standardize job titles into major ML classes.
    """

    title = str(title).lower()

    # --------------------------------------------------
    # Business Analyst Family
    # --------------------------------------------------
    if (
        "business analyst" in title
        or "business systems analyst" in title
        or "business intelligence" in title
        or "bi analyst" in title
        or "oracle business intelligence" in title
        or "crm business analyst" in title
        or "it business analyst" in title
        or "technical business analyst" in title
        or "product analyst" in title
    ):
        return "Business Analyst"

    # --------------------------------------------------
    # Data Analyst Family
    # --------------------------------------------------
    elif "data analyst" in title:
        return "Data Analyst"

    # --------------------------------------------------
    # Data Engineer Family
    # --------------------------------------------------
    elif "data engineer" in title:
        return "Data Engineer"

    # --------------------------------------------------
    # Data Scientist Family
    # --------------------------------------------------
    elif "data scientist" in title:
        return "Data Scientist"

    # --------------------------------------------------
    # AI / ML Family
    # --------------------------------------------------
    elif (
        "machine learning" in title
        or "ai engineer" in title
        or "generative ai" in title
        or "gen ai" in title
    ):
        return "AI / ML Engineer"

    # --------------------------------------------------
    # Everything Else
    # --------------------------------------------------
    else:
        return "Other"


# --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    samples = [
        "Senior Business Analyst",
        "Data Engineer",
        "Lead Data Scientist",
        "Principal AI Engineer",
        "Machine Learning Engineer - GenAI",
        "Business Intelligence Analyst",
        "Online Data Analyst",
        "Director of Analytics"
    ]

    for title in samples:

        print(title, " --> ", standardize_title(title))