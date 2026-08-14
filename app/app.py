"""
=========================================================
AI-Powered Job Posting Analyzer
PGDBA Capstone Project
=========================================================
"""

# --------------------------------------------------------
# Imports
# --------------------------------------------------------

import sys
import json
from pathlib import Path

# --------------------------------------------------------
# Project Root
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------------
# Third Party
# --------------------------------------------------------

import streamlit as st

# --------------------------------------------------------
# Backend
# --------------------------------------------------------

from src.ai.extraction.extractor import SkillExtractor
from src.normalization.pipeline import NormalizationPipeline
from src.ml.predict_job_role import JobRolePredictor
from src.career.skill_gap import SkillGapEngine
from database.db import DatabaseManager

import database.db


# --------------------------------------------------------
# Components
# --------------------------------------------------------

from components.sidebar import render_sidebar
from components.header import render_header
from components.input_panel import render_input_panel
from components.results import render_results
from components.prediction import render_prediction
from components.downloads import render_downloads
from components.footer import render_footer
from components.skill_gap import render_skill_gap
from components.explainable_ai import render_explainable_ai
from components.dashboard import render_dashboard
from components.history import render_history

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="AI Job Posting Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# Load Backend
# --------------------------------------------------------

@st.cache_resource
def load_backend():

    extractor = SkillExtractor()

    normalizer = NormalizationPipeline()

    predictor = JobRolePredictor()

    skill_gap = SkillGapEngine()

    database = DatabaseManager()

    return (
        extractor,
        normalizer,
        predictor,
        skill_gap,
        database
    )


extractor, normalizer, predictor, skill_gap, database = load_backend()

# ========================================================
# UI
# ========================================================

render_sidebar()

developer_mode = st.sidebar.toggle(
    "🛠 Developer Mode",
    value=False
)

render_header()

analyze_button, job_description = render_input_panel()

# ========================================================
# AI Pipeline
# ========================================================

if analyze_button:

    if not job_description.strip():

        st.warning("Please paste a job description.")

    else:

        with st.spinner("Analyzing Job Description..."):

            # ------------------------------------------------
            # AI Skill Extraction
            # ------------------------------------------------

            extracted = extractor.extract(
                job_id="streamlit_demo",
                description=job_description
            )

            # ------------------------------------------------
            # DEBUG 1
            # ------------------------------------------------

            if developer_mode:

             st.subheader("DEBUG 1 - Raw Extractor Output")
             st.json(extracted)

            # ------------------------------------------------
            # Skill Normalization
            # ------------------------------------------------

            normalized = normalizer.normalize_job(
                extracted
            )

            # ------------------------------------------------
            # DEBUG 2
            # ------------------------------------------------

            if developer_mode:

             st.subheader("DEBUG 2 - Normalized Output")
             st.json(normalized)

            # ------------------------------------------------
            # Combine Skills for ML / Skill Gap
            #
            # `technical_skills` alone was missing every skill the
            # extractor put under `tools` (Python, SQL, Power BI,
            # Tableau, Excel, Azure, ...). Those never reached the ML
            # model or the skill-gap engine, so they showed up as
            # "missing skills" even when clearly present in the job
            # posting. `normalized["tools_normalized"]` now carries
            # those same tools through ConfidenceEngine in the same
            # {original, normalized, skill_type, ...} shape as
            # technical_skills, so we merge both lists into one
            # complete picture before anything downstream uses it.
            # ------------------------------------------------

            all_skills = (
                normalized["technical_skills"]
                + normalized["tools_normalized"]
            )

            # ------------------------------------------------
            # Machine Learning Prediction
            # ------------------------------------------------

            prediction = predictor.predict(
                all_skills
            )

            # ------------------------------------------------
            # DEBUG 3
            # ------------------------------------------------

            if developer_mode:

             st.subheader("DEBUG 3 - Skills Sent to ML")
             st.json(all_skills)

            # ------------------------------------------------
            # Top Predictions
            # ------------------------------------------------

            top_predictions = predictor.predict_top_n(
                all_skills
            )

            # ------------------------------------------------
            # Skill Gap Analysis
            # ------------------------------------------------

            skill_gap_result = skill_gap.analyze(
                prediction["predicted_role"],
                all_skills
            )

            # ------------------------------------------------
            # Results
            # ------------------------------------------------

            render_results(
                normalized
            )

            render_prediction(
                prediction,
                top_predictions
            )

            render_skill_gap(
                skill_gap_result
            )

            render_explainable_ai(
                prediction,
                normalized
            )

            render_dashboard(
                normalized
            )

            render_history(database)


            # ------------------------------------------------
            # Save Analysis to Database
            # ------------------------------------------------

            database.execute(

                """
                INSERT INTO analysis_history (

                    predicted_role,
                    confidence,
                    education,
                    experience,
                    technical_skills,
                    normalized_skills,
                    tools,
                    soft_skills,
                    certifications,
                    skill_gap

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (

                    prediction["predicted_role"],

                    prediction["confidence"],

                    normalized.get("education"),

                    normalized.get("experience"),

                    json.dumps(extracted.get("technical_skills", [])),

                    json.dumps(all_skills),

                    json.dumps(extracted.get("tools", [])),

                    json.dumps(extracted.get("soft_skills", [])),

                    json.dumps(extracted.get("certifications", [])),

                    json.dumps(skill_gap_result)

                )

            )

            render_downloads(
                extracted,
                normalized,
                prediction
            )

            render_footer()