"""
=========================================================
Recruitment Analytics Charts
PGDBA Capstone Project
=========================================================
"""

import os

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------------
# Output Folder
# --------------------------------------------------------

OUTPUT_FOLDER = "reports/EDA_Charts/Recruitment"


# --------------------------------------------------------
# Reusable Bar Chart Function
# --------------------------------------------------------

def save_bar_chart(
    data,
    title,
    xlabel,
    ylabel,
    filename,
    color="steelblue"
):

    plt.figure(figsize=(14, 7))

    data = data.sort_values(ascending=False)

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
# Recruitment Analytics
# --------------------------------------------------------

def generate_recruitment_analytics(df):

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    # --------------------------------------------------
    # Job Title Distribution
    # --------------------------------------------------

    if "title" in df.columns:

        job_titles = (
            df["title"]
            .value_counts()
            .head(15)
        )

        save_bar_chart(
            job_titles,
            "Job Title Distribution",
            "Job Title",
            "Number of Postings",
            "01_Job_Title_Distribution.png"
        )

        print("✓ Job Title Distribution Created")

    # --------------------------------------------------
    # Top Hiring Companies
    # --------------------------------------------------

    if "company_name" in df.columns:

        companies = (
            df["company_name"]
            .value_counts()
            .head(15)
        )

        save_bar_chart(
            companies,
            "Top Hiring Companies",
            "Company",
            "Job Count",
            "02_Top_Hiring_Companies.png",
            "darkorange"
        )

        print("✓ Top Hiring Companies Created")

    # --------------------------------------------------
    # Job Locations
    # --------------------------------------------------

    if "location" in df.columns:

        locations = (
            df["location"]
            .value_counts()
            .head(15)
        )

        save_bar_chart(
            locations,
            "Top Job Locations",
            "Location",
            "Job Count",
            "03_Job_Locations.png",
            "forestgreen"
        )

        print("✓ Job Locations Created")

    # --------------------------------------------------
    # Employment Type
    # --------------------------------------------------

    if "formatted_work_type" in df.columns:

        employment = (
            df["formatted_work_type"]
            .fillna("Not Specified")
            .value_counts()
        )

        save_bar_chart(
            employment,
            "Employment Type",
            "Employment Type",
            "Count",
            "04_Employment_Type.png",
            "purple"
        )

        print("✓ Employment Type Created")

    # --------------------------------------------------
    # Experience Level
    # --------------------------------------------------

    if "formatted_experience_level" in df.columns:

        experience = (
            df["formatted_experience_level"]
            .fillna("Not Specified")
            .value_counts()
        )

        save_bar_chart(
            experience,
            "Experience Level",
            "Experience Level",
            "Count",
            "05_Experience_Level.png",
            "teal"
        )

        print("✓ Experience Level Created")

    # --------------------------------------------------
    # Remote vs On-site Jobs
    # --------------------------------------------------

    if "remote_allowed" in df.columns:

        remote = (
            df["remote_allowed"]
            .fillna(False)
            .replace({
                True: "Remote",
                False: "On-site / Hybrid"
            })
            .value_counts()
        )

        save_bar_chart(
            remote,
            "Remote vs On-site Jobs",
            "Work Mode",
            "Number of Jobs",
            "06_Remote_vs_Onsite.png",
            "royalblue"
        )

        print("✓ Remote vs On-site Jobs Created")

    # --------------------------------------------------
    # Salary Distribution
    # --------------------------------------------------

    if "normalized_salary" in df.columns:

        salary = df["normalized_salary"].dropna()

        if len(salary) > 0:

            plt.figure(figsize=(14, 7))

            plt.hist(
                salary,
                bins=30,
                color="seagreen",
                edgecolor="black"
            )

            plt.title(
                "Salary Distribution",
                fontsize=18,
                weight="bold"
            )

            plt.xlabel("Normalized Salary")

            plt.ylabel("Number of Jobs")

            plt.grid(alpha=0.3)

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    OUTPUT_FOLDER,
                    "07_Salary_Distribution.png"
                ),
                dpi=300,
                facecolor="white",
                bbox_inches="tight"
            )

            plt.close()

            print("✓ Salary Distribution Created")

    # --------------------------------------------------
    # Applications Distribution
    # --------------------------------------------------

    if "applies" in df.columns:

        applies = df["applies"].dropna()

        if len(applies) > 0:

            plt.figure(figsize=(14, 7))

            plt.hist(
                applies,
                bins=30,
                color="darkorange",
                edgecolor="black"
            )

            plt.title(
                "Applications Distribution",
                fontsize=18,
                weight="bold"
            )

            plt.xlabel("Applications")

            plt.ylabel("Number of Jobs")

            plt.grid(alpha=0.3)

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    OUTPUT_FOLDER,
                    "08_Applications_Distribution.png"
                ),
                dpi=300,
                facecolor="white",
                bbox_inches="tight"
            )

            plt.close()

            print("✓ Applications Distribution Created")

    # --------------------------------------------------
    # Job Views Distribution
    # --------------------------------------------------

    if "views" in df.columns:

        views = df["views"].dropna()

        if len(views) > 0:

            plt.figure(figsize=(14, 7))

            plt.hist(
                views,
                bins=30,
                color="mediumpurple",
                edgecolor="black"
            )

            plt.title(
                "Job Views Distribution",
                fontsize=18,
                weight="bold"
            )

            plt.xlabel("Views")

            plt.ylabel("Number of Jobs")

            plt.grid(alpha=0.3)

            plt.tight_layout()

            plt.savefig(
                os.path.join(
                    OUTPUT_FOLDER,
                    "09_Job_Views_Distribution.png"
                ),
                dpi=300,
                facecolor="white",
                bbox_inches="tight"
            )

            plt.close()

            print("✓ Job Views Distribution Created")

    print("=" * 60)
    print("Recruitment Analytics Completed Successfully")
    print(f"Charts saved to: {OUTPUT_FOLDER}")
    print("=" * 60)

    return os.listdir(OUTPUT_FOLDER)