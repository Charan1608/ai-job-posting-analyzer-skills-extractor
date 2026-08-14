"""
============================================================
ITEM 1 - DATASET SIZE & ROLE CLASS AUDIT
AI-Powered Job Posting Analyzer
============================================================

Run from project root:

    python audit_roles.py

This script DOES NOT modify any project files.
It only reads the actual CSV files and prints evidence.
============================================================
"""

from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

NORMALIZED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized_jobs.csv"
)

GOLD_STANDARD_FILE = (
    PROJECT_ROOT
    / "data"
    / "labelled"
    / "gold_standard_200.csv"
)

RAW_AI_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sample_200_with_ai_skills.csv"
)


# ============================================================
# HELPER
# ============================================================

def section(title):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def inspect_file(path):

    print()
    print("-" * 80)
    print(f"FILE: {path}")
    print("-" * 80)

    if not path.exists():

        print("STATUS: NOT FOUND")
        return None

    print("STATUS: FOUND")

    df = pd.read_csv(path)

    print(f"ROWS    : {len(df):,}")
    print(f"COLUMNS : {len(df.columns):,}")

    print()
    print("COLUMNS:")

    for i, column in enumerate(df.columns, start=1):

        print(f"{i:3}. {column}")

    return df


# ============================================================
# 1. FILE EXISTENCE
# ============================================================

section("1. PROJECT DATA FILES")

print(
    f"Normalized jobs      : "
    f"{NORMALIZED_FILE.exists()}"
)

print(
    f"Gold standard        : "
    f"{GOLD_STANDARD_FILE.exists()}"
)

print(
    f"AI extraction output : "
    f"{RAW_AI_FILE.exists()}"
)


# ============================================================
# 2. NORMALIZED JOBS
# ============================================================

section("2. NORMALIZED JOBS DATASET")

df = inspect_file(NORMALIZED_FILE)


if df is not None:

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    print()
    print("REQUIRED ROLE COLUMNS")

    for column in [
        "job_id",
        "title",
        "normalized_role",
    ]:

        print(
            f"{column:25} : "
            f"{'FOUND' if column in df.columns else 'NOT FOUND'}"
        )

    # --------------------------------------------------------
    # Total rows
    # --------------------------------------------------------

    print()
    print("TOTAL DATASET SIZE")

    print(
        f"Total rows : {len(df):,}"
    )

    # --------------------------------------------------------
    # Missing roles
    # --------------------------------------------------------

    if "normalized_role" in df.columns:

        print()
        print("ROLE COMPLETENESS")

        missing = (
            df["normalized_role"]
            .isna()
            .sum()
        )

        blank = (
            df["normalized_role"]
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        print(
            f"Missing normalized_role : {missing:,}"
        )

        print(
            f"Blank normalized_role   : {blank:,}"
        )

        # ----------------------------------------------------
        # Unique roles
        # ----------------------------------------------------

        role_series = (
            df["normalized_role"]
            .fillna("MISSING")
            .astype(str)
            .str.strip()
        )

        print()
        print("ROLE SUMMARY")

        print(
            f"Unique normalized roles : "
            f"{role_series.nunique():,}"
        )

        # ----------------------------------------------------
        # Class distribution
        # ----------------------------------------------------

        print()
        print("=" * 80)
        print("FINAL ROLE-CLASS DISTRIBUTION")
        print("=" * 80)

        role_counts = (
            role_series
            .value_counts()
            .rename_axis("normalized_role")
            .reset_index(name="job_count")
        )

        role_counts["percentage"] = (
            role_counts["job_count"]
            / len(df)
            * 100
        )

        print(
            role_counts.to_string(
                index=False,
                formatters={
                    "percentage": "{:.2f}%".format
                }
            )
        )

        # ----------------------------------------------------
        # Save role distribution
        # ----------------------------------------------------

        output_file = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "role_class_distribution_audit.csv"
        )

        role_counts.to_csv(
            output_file,
            index=False
        )

        print()
        print(
            "ROLE DISTRIBUTION SAVED:"
        )

        print(output_file)

    else:

        print(
            "\nERROR: normalized_role column not found."
        )


# ============================================================
# 3. ORIGINAL TITLE → NORMALIZED ROLE
# ============================================================

section("3. ORIGINAL TITLE → NORMALIZED ROLE")

if df is not None:

    if (
        "title" in df.columns
        and "normalized_role" in df.columns
    ):

        mapping = (
            df[
                [
                    "title",
                    "normalized_role"
                ]
            ]
            .drop_duplicates()
            .sort_values(
                [
                    "normalized_role",
                    "title"
                ]
            )
        )

        print(
            mapping.to_string(
                index=False
            )
        )

        mapping_file = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "role_title_mapping_audit.csv"
        )

        mapping.to_csv(
            mapping_file,
            index=False
        )

        print()
        print(
            "TITLE → ROLE MAPPING SAVED:"
        )

        print(mapping_file)

    else:

        print(
            "Required columns not found."
        )


# ============================================================
# 4. POSSIBLE MULTI-ROLE TITLES
# ============================================================

section("4. POSSIBLE MULTI-ROLE / HYBRID TITLES")

if df is not None and "title" in df.columns:

    title_series = (
        df["title"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # These are only indicators.
    # They do NOT automatically mean a posting is multi-role.

    multi_role_pattern = (
        r"\s/\s"
        r"|/"
        r"|\s&\s"
        r"|\band\b"
        r"|\-.*\b(?:and|&)\b"
        r"|\b(?:analyst|engineer|scientist|manager|developer)"
        r".*\b(?:analyst|engineer|scientist|manager|developer)\b"
    )

    possible_multi = df[
        title_series.str.contains(
            multi_role_pattern,
            case=False,
            regex=True,
            na=False
        )
    ].copy()

    print(
        f"Possible multi-role/hybrid titles "
        f"(indicator only): {len(possible_multi):,}"
    )

    if len(possible_multi) > 0:

        columns = [
            c
            for c in [
                "job_id",
                "title",
                "normalized_role"
            ]
            if c in possible_multi.columns
        ]

        print()
        print(
            possible_multi[
                columns
            ].to_string(index=False)
        )

        output_file = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "possible_multi_role_titles.csv"
        )

        possible_multi[
            columns
        ].to_csv(
            output_file,
            index=False
        )

        print()
        print(
            "POSSIBLE MULTI-ROLE TITLES SAVED:"
        )

        print(output_file)

else:

    print(
        "Title column not available."
    )


# ============================================================
# 5. POSSIBLE AMBIGUOUS ROLE MAPPINGS
# ============================================================

section("5. POSSIBLE AMBIGUOUS ROLE MAPPINGS")

if (
    df is not None
    and "title" in df.columns
    and "normalized_role" in df.columns
):

    # Find original titles that map to multiple
    # normalized roles.

    ambiguity = (
        df[
            [
                "title",
                "normalized_role"
            ]
        ]
        .drop_duplicates()
        .groupby("title")["normalized_role"]
        .nunique()
        .reset_index(
            name="normalized_role_count"
        )
    )

    ambiguous = ambiguity[
        ambiguity["normalized_role_count"] > 1
    ]

    print(
        "Titles mapping to multiple normalized roles:"
    )

    print(
        ambiguous.to_string(
            index=False
        )
    )

    print()
    print(
        f"Number of ambiguous title patterns: "
        f"{len(ambiguous):,}"
    )

else:

    print(
        "Required columns not available."
    )


# ============================================================
# 6. GOLD STANDARD
# ============================================================

section("6. GOLD STANDARD DATASET")

gold_df = inspect_file(
    GOLD_STANDARD_FILE
)

if gold_df is not None:

    print()
    print("GOLD STANDARD ROLE-RELATED COLUMNS")

    role_columns = [
        c
        for c in gold_df.columns
        if (
            "role" in c.lower()
            or "title" in c.lower()
            or "label" in c.lower()
        )
    ]

    if role_columns:

        for column in role_columns:

            print(
                f"\nCOLUMN: {column}"
            )

            print(
                gold_df[column]
                .value_counts(
                    dropna=False
                )
                .to_string()
            )

    else:

        print(
            "No role/title/label columns "
            "identified automatically."
        )


# ============================================================
# 7. AI EXTRACTION DATASET
# ============================================================

section("7. AI EXTRACTION DATASET")

ai_df = inspect_file(
    RAW_AI_FILE
)

if ai_df is not None:

    print()
    print(
        "AI EXTRACTION DATASET SIZE:"
    )

    print(
        f"{len(ai_df):,} rows"
    )

    print()
    print(
        "ANNOTATION COLUMNS:"
    )

    for column in [
        "annotator",
        "review_status",
        "comments"
    ]:

        if column in ai_df.columns:

            print(
                f"\n{column}:"
            )

            print(
                ai_df[column]
                .value_counts(
                    dropna=False
                )
                .to_string()
            )


# ============================================================
# 8. FINAL WARNING
# ============================================================

section("8. INTERPRETATION RULE")

print(
    """
IMPORTANT:

The "possible multi-role" section uses title-pattern
indicators only.

It does NOT prove that a posting is genuinely multi-role.

Likewise, an empty ambiguous-role result does NOT prove
that all postings are unambiguous.

The actual project code / annotations must be checked
before we state the handling strategy in the report.

Do not calculate train/test split or classification
metrics yet.

First paste the COMPLETE OUTPUT of this script back here.
"""
)