"""
=========================================================
Footer Component
AI-Powered Job Posting Analyzer
=========================================================
"""

import streamlit as st


def render_footer():

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
### 🎓 Academic Project

**PGDBA Capstone Project**

RV Institute of Management

Bengaluru
"""
        )

    with col2:

        st.markdown(
            """
### 👨‍💻 Developed By

**Charan N**

PGDBA Student

Business Analytics
"""
        )

    with col3:

        st.markdown(
            """
### 🏢 Client

**Boston India**

AI-Powered Job Posting Analyzer

Business Analytics
"""
        )

    st.markdown("---")

    st.caption(
        "© 2026 Charan N | AI-Powered Job Posting Analyzer | PGDBA Capstone Project"
    )