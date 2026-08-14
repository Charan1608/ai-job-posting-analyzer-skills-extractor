"""
=========================================================
SAVE UTILITIES
AI Job Skill Annotation Tool
=========================================================
"""
from data_loader import save_dataset
from annotation_utils import text_to_json


def save_annotation(
    df,
    index,
    technical,
    tools,
    soft,
    certifications,
    experience,
    education,
    comments=""
):
    """
    Save reviewed annotation into dataframe.
    """

    df.loc[index, "technical_skills"] = text_to_json(technical)

    df.loc[index, "tools"] = text_to_json(tools)

    df.loc[index, "soft_skills"] = text_to_json(soft)

    df.loc[index, "certifications"] = text_to_json(certifications)

    df.loc[index, "experience"] = experience

    df.loc[index, "education"] = education

    df.loc[index, "review_status"] = "Reviewed"

    df.loc[index, "comments"] = comments

    save_dataset(df)

    return df