"""
=========================================================
Input Panel Component
=========================================================
"""

import streamlit as st


def render_input_panel():

    st.header("📄 Job Description")

    st.write(
        "Paste a complete job description below and click **Analyze Job Description**."
    )

    if "job_description" not in st.session_state:
        st.session_state.job_description = ""

    sample = """
Business Analyst

We are looking for a Business Analyst with experience in Python, SQL,
Power BI, Tableau, Excel, Statistics, Business Analysis,
Machine Learning and Azure.

Responsibilities

• Gather business requirements
• Build dashboards
• Perform data analysis
• Create reports
• Work with stakeholders

Requirements

• Bachelor's Degree
• Python
• SQL
• Power BI
"""

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📋 Load Sample",
            use_container_width=True
        ):

            st.session_state.job_description = sample

    with col2:

        if st.button(
            "🗑 Clear",
            use_container_width=True
        ):

            st.session_state.job_description = ""

    job_description = st.text_area(

        "",

        key="job_description",

        height=350,

        placeholder="Paste complete job description here..."

    )

    analyze = st.button(

        "🚀 Analyze Job Description",

        type="primary",

        use_container_width=True

    )

    return analyze, job_description