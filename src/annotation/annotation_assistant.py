"""
=========================================================
GOLD STANDARD ANNOTATION ASSISTANT v2.0
AI-Powered Job Posting Analyzer
=========================================================
"""

from pathlib import Path
import pandas as pd

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = ROOT / "data" / "labelled" / "gold_standard_200.csv"

ANNOTATOR = "Charan N"

VALID_EXPERIENCE = [
    "0-2",
    "3-5",
    "5-7",
    "7-10",
    "10+",
    ""
]

VALID_EDUCATION = [
    "Bachelor's",
    "Master's",
    "MBA",
    "PhD",
    ""
]

# -------------------------------------------------------
# Load
# -------------------------------------------------------

df = pd.read_csv(CSV_FILE)

reviewed = (
    df["review_status"]
    .fillna("")
    .str.lower()
    .eq("reviewed")
    .sum()
)

remaining = len(df) - reviewed

print("=" * 70)
print("GOLD STANDARD ANNOTATION ASSISTANT v2.0")
print("=" * 70)

print(f"Total Records : {len(df)}")
print(f"Reviewed      : {reviewed}")
print(f"Remaining     : {remaining}")

print("\nRules")
print("- Use semicolons (;)")
print("- Do not infer missing information")
print("- Type SKIP to skip a record")
print("- Type EXIT anytime to stop")

print("=" * 70)

# -------------------------------------------------------
# Annotation Loop
# -------------------------------------------------------

for index, row in df.iterrows():

    status = str(row.get("review_status", "")).strip().lower()

    if status == "reviewed":
        continue

    print("\n" + "=" * 70)
    print(f"Record {index+1} / {len(df)}")
    print("=" * 70)

    print("\nJOB TITLE")
    print(row.get("title", ""))

    print("\nCOMPANY")
    print(row.get("company_name", "Unknown"))

    print("\nLOCATION")
    print(row.get("location", ""))

    print("\nDESCRIPTION")
    print("-" * 70)
    print(row.get("description", ""))
    print("-" * 70)

    tech = input("\nTechnical Skills : ")

    if tech.upper() == "EXIT":
        break

    if tech.upper() == "SKIP":
        continue

    soft = input("Soft Skills      : ")
    tools = input("Tools            : ")
    certs = input("Certifications   : ")

    # -----------------------------
    # Experience Validation
    # -----------------------------

    while True:

        exp = input(
            "Experience (0-2 / 3-5 / 5-7 / 7-10 / 10+) : "
        )

        if exp in VALID_EXPERIENCE:
            break

        print("Invalid value.")

    # -----------------------------
    # Education Validation
    # -----------------------------

    while True:

        edu = input(
            "Education (Bachelor's/Master's/MBA/PhD) : "
        )

        if edu in VALID_EDUCATION:
            break

        print("Invalid value.")

    comments = input("Comments (optional): ")

    # ---------------------------------------------------

    df.at[index, "technical_skills"] = tech
    df.at[index, "soft_skills"] = soft
    df.at[index, "tools"] = tools
    df.at[index, "certifications"] = certs
    df.at[index, "experience"] = exp
    df.at[index, "education"] = edu
    df.at[index, "comments"] = comments

    df.at[index, "annotator"] = ANNOTATOR
    df.at[index, "review_status"] = "Reviewed"

    df.to_csv(CSV_FILE, index=False)

    reviewed += 1
    remaining -= 1

    print("\n✓ Saved Successfully")

    print(
        f"Progress : {reviewed}/{len(df)} "
        f"({reviewed/len(df)*100:.1f}%)"
    )

print("\nSession Finished.")

print(f"Reviewed : {reviewed}")
print(f"Remaining : {remaining}")