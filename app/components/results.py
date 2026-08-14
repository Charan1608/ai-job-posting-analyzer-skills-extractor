"""
=========================================================
Results Component
=========================================================
"""

import pandas as pd
import streamlit as st


def render_results(normalized):

    st.markdown("---")
    st.header("📊 Extraction Results")

    # -----------------------------------
    # Read values safely
    # -----------------------------------

    technical = normalized.get("technical_skills") or []
    soft = normalized.get("soft_skills") or []
    tools = normalized.get("tools") or []
    certifications = normalized.get("certifications") or []

    experience = normalized.get("experience")
    if experience is None:
        experience = []

    education = normalized.get("education")
    if education is None:
        education = []
    elif isinstance(education, str):
        education = [education]

    # -----------------------------------
    # Summary
    # -----------------------------------

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Technical", len(technical))
    c2.metric("Soft", len(soft))
    c3.metric("Tools", len(tools))
    c4.metric("Certificates", len(certifications))
    c5.metric("Education", len(education))
    c6.metric("Experience", len(experience))

    st.markdown("---")

    # -----------------------------------
    # Technical Skills
    # -----------------------------------

    st.subheader("💻 Normalized Technical Skills")

    if technical:

        rows = []

        for skill in technical:

            rows.append(
                {
                    "Skill": skill.get("normalized", ""),
                    "Category": skill.get("skill_type", ""),
                    "Confidence (%)": round(
                        skill.get("confidence", 0) * 100,
                        2,
                    ),
                }
            )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No technical skills detected.")

    # -----------------------------------
    # Soft Skills
    # -----------------------------------

    with st.expander("🤝 Soft Skills"):

        if soft:
            for item in soft:
                st.write("•", item)
        else:
            st.info("No soft skills detected.")

    # -----------------------------------
    # Tools
    # -----------------------------------

    with st.expander("🛠 Tools"):

        if tools:
            for item in tools:
                st.write("•", item)
        else:
            st.info("No tools detected.")

    # -----------------------------------
    # Certifications
    # -----------------------------------

    with st.expander("🏆 Certifications"):

        if certifications:
            for item in certifications:
                st.write("•", item)
        else:
            st.info("No certifications detected.")

    # -----------------------------------
    # Education
    # -----------------------------------

    with st.expander("🎓 Education"):

        if education:
            for item in education:
                st.write("•", item)
        else:
            st.info("No education detected.")

    # -----------------------------------
    # Experience
    # -----------------------------------

    with st.expander("💼 Experience"):

        if experience:
            for item in experience:
                st.write("•", item)
        else:
            st.info("No experience detected.")