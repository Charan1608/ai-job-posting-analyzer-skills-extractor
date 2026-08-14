"""
=========================================================
Analysis History Component
=========================================================
"""

import json
import pandas as pd
import streamlit as st


def render_history(database):

    st.markdown("---")
    st.header("📚 Analysis History")

    rows = database.fetchall(
        """
        SELECT
            id,
            analysis_date,
            predicted_role,
            confidence,
            education,
            technical_skills
        FROM analysis_history
        ORDER BY id DESC
        """
    )

    if not rows:
        st.info("No previous analyses found.")
        return

    history = []

    for row in rows:

        history.append(
            {
                "ID": row["id"],
                "Date": row["analysis_date"],
                "Predicted Role": row["predicted_role"],
                "Confidence (%)": round(row["confidence"] * 100, 2),
                "Education": row["education"],
                "Technical Skills": ", ".join(
                    json.loads(row["technical_skills"])
                ),
            }
        )

    df = pd.DataFrame(history)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "📥 Download History",
        data=df.to_csv(index=False),
        file_name="analysis_history.csv",
        mime="text/csv"
    )