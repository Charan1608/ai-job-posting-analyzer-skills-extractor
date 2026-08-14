"""
=========================================================
Prediction Component
=========================================================
"""

import streamlit as st
import plotly.express as px


def render_prediction(prediction, top_predictions):

    st.divider()

    st.header("🎯 AI Job Role Prediction")

    predicted_role = prediction["predicted_role"]
    confidence = prediction["confidence"]

    # ----------------------------------------------------
    # Prediction Summary
    # ----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Predicted Role",
            predicted_role
        )

    with col2:

        if confidence is not None:

            st.metric(
                "Confidence",
                f"{confidence:.2%}"
            )

            if confidence >= 0.90:

                st.success(
                    f"🟢 Very High Confidence ({confidence:.2%})"
                )

            elif confidence >= 0.75:

                st.info(
                    f"🔵 High Confidence ({confidence:.2%})"
                )

            elif confidence >= 0.50:

                st.warning(
                    f"🟡 Moderate Confidence ({confidence:.2%})"
                )

            else:

                st.error(
                    f"🔴 Low Confidence ({confidence:.2%})"
                )

        else:

            st.metric(
                "Confidence",
                "N/A"
            )

    with col3:

        if top_predictions is not None:

            st.metric(
                "Candidate Roles",
                len(top_predictions)
            )

        else:

            st.metric(
                "Candidate Roles",
                "1"
            )

    with col4:

        st.metric(
            "Prediction Status",
            "Completed"
        )

    st.divider()

    # ----------------------------------------------------
    # Confidence
    # ----------------------------------------------------

    st.subheader("Prediction Confidence")

    if confidence is not None:

        st.progress(float(confidence))

    else:

        st.info("Confidence score unavailable.")

    st.divider()

    # ----------------------------------------------------
    # Top Predictions
    # ----------------------------------------------------

    st.subheader("Top Role Probabilities")

    if top_predictions is not None:

        display = (
            top_predictions
            .sort_values(
                "Probability",
                ascending=False
            )
            .copy()
        )

        display["Probability (%)"] = (
            display["Probability"] * 100
        ).round(2)

        st.success(
            f"🏆 Highest Probability Role: **{predicted_role}**"
        )

        fig = px.bar(
            display,
            x="Probability (%)",
            y="Role",
            orientation="h",
            text="Probability (%)",
            title="Role Prediction Probability Distribution"
        )

        fig.update_layout(
            height=500,
            showlegend=False,
            font=dict(size=15),
            yaxis=dict(categoryorder="total ascending"),
            xaxis_title="Probability (%)",
            yaxis_title=""
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            display[
                ["Role", "Probability (%)"]
            ],
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            "Predictions are generated using normalized ESCO skills extracted from the job description."
        )

    else:

        st.info(
            "Probability distribution unavailable."
        )

    st.divider()

    # ----------------------------------------------------
    # Model Information
    # ----------------------------------------------------

    with st.expander("🧠 Machine Learning Model Details"):

        st.markdown(
            """
## Machine Learning Model

| Item | Value |
|------|------|
| Algorithm | Logistic Regression |
| Dataset | LinkedIn Job Postings |
| Feature Engineering | Binary Skill Encoding |
| Selected Features | 68 |
| Target Roles | 6 |
| Explainability | Feature-based |
| Skill Normalization | ESCO Taxonomy |
| AI Extraction | Groq LLM |

---

### Prediction Pipeline

Job Description

⬇

AI Skill Extraction

⬇

ESCO Skill Normalization

⬇

Feature Engineering

⬇

Machine Learning Prediction

⬇

Career Recommendation

---

The confidence score represents the probability assigned by the trained Logistic Regression model.
"""
        )

    st.divider()