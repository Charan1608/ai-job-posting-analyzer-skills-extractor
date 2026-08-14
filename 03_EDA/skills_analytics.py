"""
=========================================================
Skills Analytics
PGDBA Capstone Project
=========================================================
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

import json
from collections import Counter


# --------------------------------------------------------
# Output Folder
# --------------------------------------------------------

OUTPUT_FOLDER = "reports/EDA_Charts/Skills"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# --------------------------------------------------------
# Save Bar Chart
# --------------------------------------------------------

def save_bar_chart(
    data,
    title,
    xlabel,
    ylabel,
    filename,
    color="steelblue"
):

    if len(data) == 0:
        return

    plt.figure(figsize=(14,7))

    data = data.sort_values(
        ascending=False
    )

    ax = data.plot(
        kind="bar",
        color=color
    )

    for container in ax.containers:

        ax.bar_label(
            container,
            fontsize=9
        )

    plt.title(
        title,
        fontsize=18,
        weight="bold"
    )

    plt.xlabel(
        xlabel,
        fontsize=13
    )

    plt.ylabel(
        ylabel,
        fontsize=13
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(
            OUTPUT_FOLDER,
            filename
        ),

        dpi=300,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close()


# --------------------------------------------------------
# Skills Analytics
# --------------------------------------------------------

def generate_skills_analytics():

    # Renamed from `skills` -> `skills_df` so it can never be
    # accidentally shadowed by the per-row skill list built later
    # in the Soft Skills section (see `skill_list` below). Any
    # variable named `skills` that shadows this DataFrame turns
    # every later `skills["column"]` lookup into a TypeError, since
    # it silently becomes a plain Python list instead.
    skills_df = pd.read_csv(
        "data/processed/normalized_skills_long.csv"
    )

    frequency = pd.read_csv(
        "data/processed/skill_frequency.csv"
    )

    print("="*60)
    print("Generating Skills Analytics")
    print("="*60)

    # --------------------------------------------------
    # Figure 10
    # Top Technical Skills
    # --------------------------------------------------

    top_skills = (

        frequency

        .sort_values(
            "frequency",
            ascending=False
        )

        .head(20)

        .set_index("skill")["frequency"]

    )

    save_bar_chart(

        top_skills,

        "Top Technical Skills",

        "Skill",

        "Frequency",

        "10_Top_Technical_Skills.png",

        "royalblue"

    )

    print("✓ Top Technical Skills Created")

    # --------------------------------------------------
    # Programming Languages
    # --------------------------------------------------

    programming = [

        "Python",

        "R",

        "SQL",

        "Java",

        "Scala",

        "Julia",

        "SAS",

        "MATLAB",

        "C++",

        "C#",

        "JavaScript",

        "TypeScript"

    ]

    programming_df = skills_df[

        skills_df["normalized_skill"]

        .isin(programming)

    ]

    programming_chart = (

        programming_df

        ["normalized_skill"]

        .value_counts()

    )

    save_bar_chart(

        programming_chart,

        "Programming Languages",

        "Language",

        "Frequency",

        "11_Programming_Languages.png",

        "green"

    )

    print("✓ Programming Languages Created")

    # --------------------------------------------------
    # BI Tools
    # --------------------------------------------------

    bi_tools = [

        "Power BI",

        "Tableau",

        "Microsoft Excel",

        "Excel",

        "Looker",

        "Qlik",

        "MicroStrategy"

    ]

    bi_df = skills_df[

        skills_df["normalized_skill"]

        .isin(bi_tools)

    ]

    bi_chart = (

        bi_df

        ["normalized_skill"]

        .value_counts()

    )

    save_bar_chart(

        bi_chart,

        "Business Intelligence Tools",

        "Tool",

        "Frequency",

        "12_BI_Tools.png",

        "darkorange"

    )

    print("✓ BI Tools Created")

    # --------------------------------------------------
    # Cloud Technologies
    # --------------------------------------------------

    cloud = [

        "Amazon Web Services",

        "AWS",

        "Microsoft Azure",

        "Azure",

        "Google Cloud",

        "Snowflake",

        "Databricks",

        "BigQuery",

        "Redshift",

        "Azure Synapse",

        "Amazon S3",

        "Amazon EC2",

        "Microsoft Fabric"

    ]

    cloud_df = skills_df[

        skills_df["normalized_skill"]

        .isin(cloud)

    ]

    cloud_chart = (

        cloud_df

        ["normalized_skill"]

        .value_counts()

    )

    save_bar_chart(

        cloud_chart,

        "Cloud Technologies",

        "Technology",

        "Frequency",

        "13_Cloud_Technologies.png",

        "purple"

    )

    print("✓ Cloud Technologies Created")

    # --------------------------------------------------
    # AI / ML Skills
    # --------------------------------------------------

    ai = [

        "Machine Learning",

        "Deep Learning",

        "Artificial Intelligence",

        "TensorFlow",

        "PyTorch",

        "Keras",

        "Scikit-learn",

        "Natural Language Processing",

        "Computer Vision",

        "Generative AI",

        "Large Language Models",

        "LLM",

        "OpenAI",

        "LangChain",

        "Hugging Face"

    ]

    ai_df = skills_df[

        skills_df["normalized_skill"]

        .isin(ai)

    ]

    ai_chart = (

        ai_df

        ["normalized_skill"]

        .value_counts()

    )

    save_bar_chart(

        ai_chart,

        "AI / Machine Learning Skills",

        "Skill",

        "Frequency",

        "14_AI_ML_Skills.png",

        "crimson"

    )

    print("✓ AI / ML Skills Created")

    # --------------------------------------------------
    # Soft Skills
    # --------------------------------------------------

    jobs_df = pd.read_csv(
        "data/processed/normalized_jobs.csv"
    )

    soft_counter = Counter()

    for value in jobs_df["soft_skills"].fillna("[]"):

        try:

            # Renamed from `skills` -> `skill_list`. This used to
            # reassign the module-level `skills` DataFrame to a plain
            # list on every loop iteration, so any code after this
            # loop that expected `skills` to still be a DataFrame
            # (e.g. `skills["category"]`) would raise
            # `TypeError: list indices must be integers or slices,
            # not str`.
            skill_list = json.loads(value)

            for skill in skill_list:

                skill = skill.strip()

                if skill:

                    soft_counter[skill] += 1

        except Exception:

            pass

    if soft_counter:

        soft_chart = (

            pd.Series(soft_counter)

            .sort_values(
                ascending=False
            )

            .head(20)

        )

        save_bar_chart(

            soft_chart,

            "Top Soft Skills",

            "Soft Skill",

            "Frequency",

            "15_Soft_Skills.png",

            "teal"

        )

        print("✓ Soft Skills Created")

    # --------------------------------------------------
    # Certifications
    # --------------------------------------------------

    cert_counter = Counter()

    for value in jobs_df["certifications"].fillna("[]"):

        try:

            cert_list = json.loads(value)

            for cert in cert_list:

                cert = cert.strip()

                if cert:

                    cert_counter[cert] += 1

        except Exception:

            pass

    if cert_counter:

        cert_chart = (

            pd.Series(cert_counter)

            .sort_values(
                ascending=False
            )

            .head(20)

        )

        save_bar_chart(

            cert_chart,

            "Professional Certifications",

            "Certification",

            "Frequency",

            "16_Certifications.png",

            "darkorange"

        )

        print("✓ Certifications Created")

    # --------------------------------------------------
    # Skill Categories
    # --------------------------------------------------

    category_chart = (

        skills_df["category"]

        .dropna()

        .value_counts()

        .head(15)

    )

    save_bar_chart(

        category_chart,

        "Skill Categories",

        "Category",

        "Frequency",

        "17_Skill_Categories.png",

        "mediumseagreen"

    )

    print("✓ Skill Categories Created")


    # --------------------------------------------------
    # Normalization Methods
    # --------------------------------------------------

    method_chart = (

        skills_df["method"]

        .fillna("Unknown")

        .value_counts()

    )

    save_bar_chart(

        method_chart,

        "Normalization Methods",

        "Method",

        "Frequency",

        "18_Normalization_Methods.png",

        "darkorange"

    )

    print("✓ Normalization Methods Created")


    # --------------------------------------------------
    # Confidence Distribution
    # --------------------------------------------------

    confidence = (

        skills_df["confidence"]

        .dropna()

    )

    if len(confidence) > 0:

        plt.figure(figsize=(14,7))

        plt.hist(

            confidence,

            bins=20,

            color="royalblue",

            edgecolor="black"

        )

        plt.title(

            "Confidence Distribution",

            fontsize=18,

            weight="bold"

        )

        plt.xlabel("Confidence Score")

        plt.ylabel("Frequency")

        plt.grid(alpha=0.3)

        plt.tight_layout()

        plt.savefig(

            os.path.join(

                OUTPUT_FOLDER,

                "19_Confidence_Distribution.png"

            ),

            dpi=300,

            facecolor="white",

            bbox_inches="tight"

        )

        plt.close()

        print("✓ Confidence Distribution Created")


    # --------------------------------------------------
    # ESCO Coverage
    # --------------------------------------------------

    matched = skills_df["esco_uri"].notna().sum()

    unmatched = skills_df["esco_uri"].isna().sum()

    coverage = pd.Series({

        "ESCO Matched": matched,

        "Not Matched": unmatched

    })

    save_bar_chart(

        coverage,

        "ESCO Skill Coverage",

        "Coverage",

        "Count",

        "20_ESCO_Coverage.png",

        "crimson"

    )

    print("✓ ESCO Coverage Created")


    # --------------------------------------------------
    # Average Confidence by Matching Method
    #
    # Figures 18-20 show how often each method was used and the
    # overall confidence distribution and ESCO coverage, but not how
    # well each individual method performed. This ties method choice
    # directly to normalization quality -- e.g. a method used often
    # but with low average confidence is a candidate for review.
    # --------------------------------------------------

    avg_confidence = (

        skills_df

        .groupby("method")["confidence"]

        .mean()

        .sort_values(ascending=False)

    )

    save_bar_chart(

        avg_confidence,

        "Average Confidence by Matching Method",

        "Matching Method",

        "Average Confidence",

        "21_Average_Confidence_by_Method.png",

        "dodgerblue"

    )

    print("✓ Average Confidence by Method Created")


    print("=" * 60)
    print("Skills Analytics Completed Successfully")
    print("=" * 60)