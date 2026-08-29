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
import hashlib
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


# ========================================================
# PAGE CONFIGURATION
# ========================================================

st.set_page_config(
    page_title="AI Job Posting Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ========================================================
# LOAD BACKEND
# ========================================================

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
# USER INTERFACE
# ========================================================

render_sidebar()

developer_mode = st.sidebar.toggle(
    "🛠 Developer Mode",
    value=False
)

render_header()

analyze_button, job_description = render_input_panel()


# ========================================================
# AI PIPELINE
# ========================================================

if analyze_button:

    # ----------------------------------------------------
    # Validate Input
    # ----------------------------------------------------

    if not job_description.strip():

        st.warning(
            "Please paste a job description."
        )

    else:

        try:

            with st.spinner(
                "Analyzing Job Description..."
            ):

                # =================================================
                # 1. AI SKILL EXTRACTION
                # =================================================

                # Create a unique job ID from the actual
                # job description.
                #
                # This prevents an old cached
                # "streamlit_demo" result from being reused.

                analysis_job_id = (
                    "streamlit_demo_"
                    + hashlib.sha256(
                        job_description.encode("utf-8")
                    ).hexdigest()[:12]
                )

                extracted = extractor.extract(
                    job_id=analysis_job_id,
                    description=job_description
                )


                # -------------------------------------------------
                # DEBUG 1
                # -------------------------------------------------

                if developer_mode:

                    st.subheader(
                        "DEBUG 1 - Raw Extractor Output"
                    )

                    st.json(extracted)


                # =================================================
                # 2. CHECK EXTRACTION
                # =================================================

                extracted_skill_count = (
                    len(
                        extracted.get(
                            "technical_skills",
                            []
                        )
                    )
                    +
                    len(
                        extracted.get(
                            "tools",
                            []
                        )
                    )
                    +
                    len(
                        extracted.get(
                            "soft_skills",
                            []
                        )
                    )
                    +
                    len(
                        extracted.get(
                            "certifications",
                            []
                        )
                    )
                )


                if extracted_skill_count == 0:

                    st.error(
                        "The AI extraction returned no skills. "
                        "Please check the Groq API/model configuration."
                    )

                    if developer_mode:

                        st.warning(
                            "DEBUG: Extraction completed, "
                            "but all skill lists are empty."
                        )

                    st.stop()


                # =================================================
                # 3. SKILL NORMALIZATION
                # =================================================

                normalized = normalizer.normalize_job(
                    extracted
                )


                # -------------------------------------------------
                # DEBUG 2
                # -------------------------------------------------

                if developer_mode:

                    st.subheader(
                        "DEBUG 2 - Normalized Output"
                    )

                    st.json(normalized)


                # =================================================
                # 4. COMBINE TECHNICAL + TOOLS
                # =================================================

                technical_skills = normalized.get(
                    "technical_skills",
                    []
                )

                tools_normalized = normalized.get(
                    "tools_normalized",
                    []
                )

                all_skills = (
                    technical_skills
                    + tools_normalized
                )


                # -------------------------------------------------
                # DEBUG 3
                # -------------------------------------------------

                if developer_mode:

                    st.subheader(
                        "DEBUG 3 - Skills Sent to ML"
                    )

                    st.json(all_skills)


                # =================================================
                # 5. MACHINE LEARNING PREDICTION
                # =================================================

                prediction = predictor.predict(
                    all_skills
                )


                # =================================================
                # 6. TOP PREDICTIONS
                # =================================================

                top_predictions = (
                    predictor.predict_top_n(
                        all_skills
                    )
                )


                # =================================================
                # 7. SKILL GAP ANALYSIS
                # =================================================

                skill_gap_result = skill_gap.analyze(
                    prediction["predicted_role"],
                    all_skills
                )


            # =====================================================
            # DISPLAY SUCCESS
            # =====================================================

            st.success(
                "Analysis Completed Successfully!"
            )


            # =====================================================
            # RESULTS
            # =====================================================

            render_results(
                normalized
            )


            # =====================================================
            # ROLE PREDICTION
            # =====================================================

            render_prediction(
                prediction,
                top_predictions
            )


            # =====================================================
            # SKILL GAP
            # =====================================================

            render_skill_gap(
                skill_gap_result
            )


            # =====================================================
            # EXPLAINABLE AI
            # =====================================================

            render_explainable_ai(
                prediction,
                normalized
            )


            # =====================================================
            # DASHBOARD
            # =====================================================

            render_dashboard(
                normalized
            )


            # =====================================================
            # HISTORY
            # =====================================================

            render_history(
                database
            )


            # =====================================================
            # SAVE TO DATABASE
            # =====================================================

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

                    prediction.get(
                        "predicted_role"
                    ),

                    prediction.get(
                        "confidence"
                    ),

                    normalized.get(
                        "education"
                    ),

                    normalized.get(
                        "experience"
                    ),

                    json.dumps(
                        extracted.get(
                            "technical_skills",
                            []
                        )
                    ),

                    json.dumps(
                        all_skills
                    ),

                    json.dumps(
                        extracted.get(
                            "tools",
                            []
                        )
                    ),

                    json.dumps(
                        extracted.get(
                            "soft_skills",
                            []
                        )
                    ),

                    json.dumps(
                        extracted.get(
                            "certifications",
                            []
                        )
                    ),

                    json.dumps(
                        skill_gap_result
                    )

                )
            )


            # =====================================================
            # DOWNLOADS
            # =====================================================

            render_downloads(
                extracted,
                normalized,
                prediction
            )


            # =====================================================
            # FOOTER
            # =====================================================

            render_footer()


        # ========================================================
        # ERROR HANDLING
        # ========================================================

        except Exception as e:

            st.error(
                "Unable to complete the analysis."
            )

            if developer_mode:

                st.subheader(
                    "DEBUG - Application Error"
                )

                st.exception(e)

            else:

                st.info(
                    "Please enable Developer Mode and "
                    "run the analysis again to view "
                    "diagnostic information."
                )
