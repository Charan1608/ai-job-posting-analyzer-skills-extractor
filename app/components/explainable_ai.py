"""
=========================================================
Explainable AI Component
=========================================================
"""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


def render_explainable_ai(prediction, normalized):

    st.divider()

    st.header("🧠 Explainable AI")

    technical = normalized.get("technical_skills", [])

    if not technical:

        st.info("No normalized technical skills available.")

        return

    # ----------------------------------------------------
    # Prediction Explanation
    # ----------------------------------------------------

    st.success(
        f"""
The AI model predicted **{prediction['predicted_role']}**
because the extracted and normalized skills closely match
the knowledge profile learned for this role.
"""
    )

    # ----------------------------------------------------
    # Build Table
    # ----------------------------------------------------

    rows = []

    categories = []

    methods = []

    confidences = []

    for skill in technical:

        if isinstance(skill, dict):

            category = skill.get(
                "skill_type",
                "Unknown"
            )

            confidence = round(
                skill.get(
                    "confidence",
                    0
                ) * 100,
                2
            )

            method = skill.get(
                "method",
                ""
            )

            rows.append({

                "Skill":
                    skill.get(
                        "normalized",
                        ""
                    ),

                "Category":
                    category,

                "Confidence (%)":
                    confidence,

                "Method":
                    method

            })

            categories.append(category)

            methods.append(method)

            confidences.append(confidence)

    df = pd.DataFrame(rows)

    st.subheader("Detected Skills")

    st.dataframe(

        df,

        hide_index=True,

        use_container_width=True

    )

    # ----------------------------------------------------
    # Metrics
    # ----------------------------------------------------

    st.subheader("Normalization Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Skills",

            len(df)

        )

    with col2:

        st.metric(

            "Average Confidence",

            f"{sum(confidences)/len(confidences):.1f}%"

        )

    with col3:

        st.metric(

            "Normalization Methods",

            len(set(methods))

        )

    # ----------------------------------------------------
    # Category Distribution
    # ----------------------------------------------------

    st.subheader("Skill Category Distribution")

    category_df = pd.DataFrame(

        {

            "Category": list(
                Counter(categories).keys()
            ),

            "Count": list(
                Counter(categories).values()
            )

        }

    )

    fig = px.bar(

        category_df,

        x="Category",

        y="Count",

        text="Count",

        title="Detected Skill Categories"

    )

    fig.update_layout(

        height=400,

        showlegend=False

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # ----------------------------------------------------
    # Pipeline
    # ----------------------------------------------------

    with st.expander(

        "🔍 How the AI made this prediction"

    ):

        st.markdown(
            """
### End-to-End AI Pipeline

Job Description

⬇

Generative AI Skill Extraction (Groq)

⬇

ESCO Skill Normalization

⬇

Feature Engineering

⬇

Logistic Regression Classification

⬇

Job Role Prediction

⬇

Career Skill Gap Analysis

The prediction is based entirely on the normalized skills extracted from the job description and transformed into machine learning features.
"""
        )

    st.caption(
        "Explainable AI provides transparency by showing the normalized skills and categories that contributed to the final prediction."
    )