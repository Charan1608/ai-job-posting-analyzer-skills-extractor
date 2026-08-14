"""
=========================================================
Header Component
=========================================================
"""

import streamlit as st


def render_header():

    # ----------------------------------------------------
    # Hero Section
    # ----------------------------------------------------

    st.title("🤖 AI-Powered Job Posting Analyzer & Skills Intelligence Platform")

    st.markdown(
        """
### Business Analytics Role Prediction using Generative AI, ESCO Taxonomy and Machine Learning
"""
    )

    st.write(
        """
Analyze job descriptions automatically using Large Language Models,
normalize skills using the ESCO Taxonomy, engineer machine learning
features, predict the most suitable Business Analytics role, identify
skill gaps, and generate AI-powered career insights.
"""
    )

    st.divider()

    # ----------------------------------------------------
    # Platform Overview
    # ----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="🤖 AI Extraction",
            value="Active"
        )

    with col2:

        st.metric(
            label="📚 ESCO",
            value="Integrated"
        )

    with col3:

        st.metric(
            label="🧠 ML Model",
            value="Logistic Regression"
        )

    with col4:

        st.metric(
            label="🎯 Supported Roles",
            value="6"
        )

    st.divider()

    # ----------------------------------------------------
    # Supported Roles
    # ----------------------------------------------------

    st.subheader("🎯 Supported Business Analytics Roles")

    col1, col2 = st.columns(2)

    with col1:

        st.success("📊 Business Analyst")

        st.success("📈 Data Analyst")

        st.success("⚙ Data Engineer")

    with col2:

        st.success("🧠 Data Scientist")

        st.success("🤖 AI / ML Engineer")

        st.success("📌 Other Analytics Roles")

    st.divider()

    # ----------------------------------------------------
    # AI Pipeline
    # ----------------------------------------------------

    st.subheader("⚡ End-to-End AI Pipeline")

    st.info(
        """
**Job Description**
➡ **AI Skill Extraction**
➡ **ESCO Skill Normalization**
➡ **Feature Engineering**
➡ **Machine Learning**
➡ **Role Prediction**
➡ **Skill Gap Analysis**
➡ **Explainable AI**
"""
    )

    st.divider()