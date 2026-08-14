"""
=========================================================
Skill Gap Component
=========================================================
"""

import streamlit as st


def render_skill_gap(result):

    st.markdown("---")

    st.header("🎯 Skill Gap Analysis")

    score = result["score"]

    st.metric(
        "Overall Skill Match",
        f"{score}%"
    )

    st.progress(score / 100)

    col1, col2 = st.columns(2)

    # --------------------------
    # Matched Skills
    # --------------------------

    with col1:

        st.subheader("✅ Matched Skills")

        if result["matched"]:

            for skill in result["matched"]:

                st.success(skill.title())

        else:

            st.info("No matched skills")

    # --------------------------
    # Missing Skills
    # --------------------------

    with col2:

        st.subheader("❌ Missing Skills")

        if result["missing"]:

            for skill in result["missing"]:

                st.error(skill.title())

        else:

            st.success("No missing skills!")

    st.markdown("---")

    st.subheader("📚 Learning Recommendations")

    if len(result["recommendations"]) == 0:

        st.success("You already meet all required skills.")

        return

    for item in result["recommendations"]:

        with st.container():

            st.markdown(f"### 🎓 {item['skill'].title()}")

            c1, c2 = st.columns(2)

            with c1:

                st.write("**Course**")

                st.info(item["course"])

            with c2:

                st.write("**Certification**")

                st.success(item["certification"])

            st.markdown("---")