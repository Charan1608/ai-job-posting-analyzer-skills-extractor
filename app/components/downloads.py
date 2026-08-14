"""
=========================================================
Downloads Component
=========================================================
"""

import json
import pandas as pd
import streamlit as st


def render_downloads(extracted, normalized, prediction):

    st.markdown("---")

    st.header("📥 Download Results")

    result = {
        "extracted": extracted,
        "normalized": normalized,
        "prediction": prediction
    }

    json_data = json.dumps(
        result,
        indent=4,
        default=str
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📄 Download JSON",
            data=json_data,
            file_name="job_analysis.json",
            mime="application/json",
            use_container_width=True
        )

    with col2:

        rows = []

        for skill in normalized["technical_skills"]:

            rows.append({
                "Skill": skill.get("normalized", ""),
                "Category": skill.get("skill_type", ""),
                "Confidence": skill.get("confidence", 0)
            })

        csv = pd.DataFrame(rows).to_csv(index=False)

        st.download_button(
            "📊 Download CSV",
            data=csv,
            file_name="normalized_skills.csv",
            mime="text/csv",
            use_container_width=True
        )