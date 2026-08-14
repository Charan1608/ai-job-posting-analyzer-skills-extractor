"""
=========================================================
AI JOB SKILL ANNOTATION TOOL
Version 2.0
=========================================================
"""

import streamlit as st

from data_loader import load_dataset
from annotation_utils import (
    json_to_text,
    reviewed_jobs,
    remaining_jobs
)
from save_utils import save_annotation


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Job Skill Annotation Tool",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Skill Annotation Tool")

st.markdown("---")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_dataset()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "current_index" not in st.session_state:
    st.session_state.current_index = 0


current_index = st.session_state.current_index

row = df.iloc[current_index]
st.subheader("DEBUG")

st.write(type(row["technical_skills"]))

st.write(row["technical_skills"])

st.write(repr(row["technical_skills"]))

st.write(json_to_text(row["technical_skills"]))
st.write("DEBUG")
st.write(row["technical_skills"])


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("Annotation Progress")

reviewed = reviewed_jobs(df)

remaining = remaining_jobs(df)

st.sidebar.metric(
    "Reviewed",
    reviewed
)

st.sidebar.metric(
    "Remaining",
    remaining
)


# ---------------------------------------------------------
# PROGRESS BAR
# ---------------------------------------------------------

progress = (current_index + 1) / len(df)

st.progress(progress)

st.caption(
    f"Job {current_index + 1} of {len(df)}"
)
# ---------------------------------------------------------
# JOB INFORMATION
# ---------------------------------------------------------

st.markdown("---")

st.subheader("💼 Job Title")
st.info(str(row["title"]))

st.subheader("🏢 Company")
st.info(str(row["company_name"]))

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Education")
    st.info(str(row.get("education", "")))

with col2:
    st.subheader("💼 Experience")
    st.info(str(row.get("experience", "")))

st.subheader("📄 Job Description")

st.text_area(
    "",
    value=str(row["description"]),
    height=350,
    disabled=True
)
# ---------------------------------------------------------
# ANNOTATION FIELDS
# ---------------------------------------------------------

st.markdown("---")
st.header("📝 AI Extracted Skills")

technical_skills = st.text_area(
    "Technical Skills",
    value=json_to_text(row["technical_skills"]),
    height=140
)

tools = st.text_area(
    "Tools",
    value=json_to_text(row["tools"]),
    height=120
)

soft_skills = st.text_area(
    "Soft Skills",
    value=json_to_text(row["soft_skills"]),
    height=140
)

certifications = st.text_area(
    "Certifications",
    value=json_to_text(row["certifications"]),
    height=100
)

col1, col2 = st.columns(2)

with col1:
    experience = st.text_input(
        "Experience",
        value="" if str(row["experience"]) == "nan" else str(row["experience"])
    )

with col2:
    education = st.text_input(
        "Education",
        value="" if str(row["education"]) == "nan" else str(row["education"])
    )

comments = st.text_area(
    "Comments",
    value="" if str(row["comments"]) == "nan" else str(row["comments"]),
    height=120
)