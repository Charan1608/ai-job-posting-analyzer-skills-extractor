"""
=========================================================
Sidebar Component
=========================================================
"""

import streamlit as st


def render_sidebar():

    with st.sidebar:

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        st.title("🤖 AI Job Posting Analyzer")

        st.caption(
            "Business Analytics Role Prediction using\n"
            "Generative AI & Machine Learning"
        )

        st.success("🟢 System Ready")

        st.divider()

        # -------------------------------------------------
        # AI Pipeline
        # -------------------------------------------------

        st.subheader("🔄 AI Pipeline")

        pipeline = [
            "AI Skill Extraction",
            "ESCO Skill Normalization",
            "Feature Engineering",
            "Machine Learning",
            "Role Prediction",
            "Explainable AI"
        ]

        for item in pipeline:
            st.write(f"✅ {item}")

        st.divider()

        # -------------------------------------------------
        # Technology Stack
        # -------------------------------------------------

        st.subheader("🛠 Technology Stack")

        technologies = [
            "🐍 Python",
            "🧠 Groq LLM",
            "📚 ESCO Taxonomy",
            "🤗 Sentence Transformers",
            "⚙️ Scikit-learn",
            "📈 Logistic Regression",
            "🌐 Streamlit"
        ]

        for tech in technologies:
            st.write(tech)

        st.divider()

        # -------------------------------------------------
        # Machine Learning
        # -------------------------------------------------

        st.subheader("🧠 Machine Learning")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Accuracy",
                "52.5%"
            )

            st.metric(
                "Features",
                "68"
            )

        with col2:

            st.metric(
                "Weighted F1",
                "51.4%"
            )

            st.metric(
                "Roles",
                "6"
            )

        st.info("**Model:** Logistic Regression")

        st.divider()

        # -------------------------------------------------
        # Project Status
        # -------------------------------------------------

        st.subheader("📌 Project Status")

        status = [
            "AI Extraction",
            "ESCO Normalization",
            "Feature Engineering",
            "Machine Learning",
            "Explainable AI",
            "SQLite Database",
            "Dashboard"
        ]

        for item in status:
            st.success(f"✅ {item}")

        st.divider()

        # -------------------------------------------------
        # Project Information
        # -------------------------------------------------

        st.subheader("🎓 Project")

        st.markdown(
            """
**AI-Powered Job Posting Analyzer**

PGDBA Capstone Project

**Developer:** Charan N

**Institute:** RV Institute of Management

**Client:** Boston India
"""
        )

        st.divider()

        # -------------------------------------------------
        # Version
        # -------------------------------------------------

        st.caption("Version 3.0")