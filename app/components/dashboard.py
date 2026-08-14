"""
=========================================================
Analytics Dashboard
=========================================================
"""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


def render_dashboard(normalized):

    st.divider()

    st.header("📊 Skills Intelligence Dashboard")

    # ----------------------------------------------------
    # Load Data
    # ----------------------------------------------------

    technical = normalized.get("technical_skills", [])
    tools_normalized = normalized.get("tools_normalized", [])
    soft = normalized.get("soft_skills", [])

    all_skills = technical + tools_normalized

    # ----------------------------------------------------
    # Executive Summary
    # ----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Technical Skills", len(technical))

    with col2:
        st.metric("Technologies", len(tools_normalized))

    with col3:
        st.metric("Soft Skills", len(soft))

    with col4:
        st.metric("Total Skills", len(all_skills))

    st.divider()

    # ----------------------------------------------------
    # Skill Category Distribution
    # ----------------------------------------------------

    categories = []

    for skill in all_skills:

        if isinstance(skill, dict):

            category = skill.get("skill_type")

            if category:
                categories.append(category)

    if categories:

        category_df = pd.DataFrame(
            {
                "Category": list(Counter(categories).keys()),
                "Count": list(Counter(categories).values())
            }
        )

        st.subheader("📂 Skill Category Distribution")

        fig = px.bar(
            category_df,
            x="Category",
            y="Count",
            text="Count",
            title="Skills by Category"
        )

        fig.update_layout(
            height=450,
            showlegend=False,
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # Technology Distribution
    # ----------------------------------------------------

    technologies = []

    for skill in tools_normalized:

        if isinstance(skill, dict):
            technologies.append(skill.get("normalized"))

    if technologies:

        tech_df = pd.DataFrame(
            {
                "Technology": list(Counter(technologies).keys()),
                "Count": list(Counter(technologies).values())
            }
        )

        st.subheader("🛠 Technology Stack")

        fig = px.bar(
            tech_df,
            x="Technology",
            y="Count",
            text="Count",
            title="Detected Technologies"
        )

        fig.update_layout(
            height=450,
            showlegend=False,
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # Technical Skills
    # ----------------------------------------------------

    technical_names = []

    for skill in technical:

        if isinstance(skill, dict):
            technical_names.append(skill.get("normalized"))

    if technical_names:

        skill_df = pd.DataFrame(
            {
                "Skill": list(Counter(technical_names).keys()),
                "Count": list(Counter(technical_names).values())
            }
        )

        st.subheader("📈 Technical Skills")

        fig = px.bar(
            skill_df,
            x="Skill",
            y="Count",
            text="Count",
            title="Technical Skills Extracted"
        )

        fig.update_layout(
            height=450,
            showlegend=False,
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # Soft Skills
    # ----------------------------------------------------

    if soft:

        soft_df = pd.DataFrame(
            {
                "Soft Skill": list(Counter(soft).keys()),
                "Count": list(Counter(soft).values())
            }
        )

        st.subheader("🤝 Soft Skills")

        fig = px.bar(
            soft_df,
            x="Soft Skill",
            y="Count",
            text="Count",
            title="Soft Skills"
        )

        fig.update_layout(
            height=450,
            showlegend=False,
            font=dict(size=14)
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------------------
    # Dashboard Summary
    # ----------------------------------------------------

    st.divider()

    st.subheader("📋 Dashboard Summary")

    col1, col2 = st.columns(2)

    most_common_category = (
        Counter(categories).most_common(1)[0][0]
        if categories else "N/A"
    )

    most_common_tool = (
        Counter(technologies).most_common(1)[0][0]
        if technologies else "N/A"
    )

    with col1:

        st.success(
            f"🏆 Most Common Skill Category\n\n**{most_common_category}**"
        )

    with col2:

        st.success(
            f"🛠 Most Common Technology\n\n**{most_common_tool}**"
        )

    st.caption(
        "This dashboard summarizes the AI-extracted and ESCO-normalized skills detected from the job description."
    )