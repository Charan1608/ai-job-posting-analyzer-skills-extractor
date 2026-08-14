from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

NORMALIZED_FILE = ROOT / "data_processed" / "normalized_skills_pro.csv"
SUMMARY_FILE = ROOT / "data_processed" / "normalization_summary_pro.csv"
TAXONOMY_FILE = ROOT / "taxonomy" / "esco_skills.csv"

print("=" * 78)
print("7. SKILL NORMALIZATION – ESCO-ALIGNED NORMALIZATION")
print("=" * 78)

# ------------------------------------------------------------
# Load normalization output
# ------------------------------------------------------------

df = pd.read_csv(NORMALIZED_FILE)

print(f"\nNormalization File : {NORMALIZED_FILE.name}")
print(f"Records Processed  : {len(df):,}")
print(f"Columns            : {len(df.columns)}")

# ------------------------------------------------------------
# Taxonomy
# ------------------------------------------------------------

if TAXONOMY_FILE.exists():
    taxonomy = pd.read_csv(TAXONOMY_FILE)
    print(f"ESCO Taxonomy      : {len(taxonomy):,} entries")
else:
    print("ESCO Taxonomy      : File not found")

# ------------------------------------------------------------
# Detect normalization columns
# ------------------------------------------------------------

skill_columns = [
    c for c in df.columns
    if any(x in c.lower() for x in
           ["normalized", "matched", "canonical", "esco"])
]

print("\nNORMALIZATION ARTIFACT")
print("-" * 78)

if skill_columns:
    print("Normalization Fields:")
    for col in skill_columns[:10]:
        print(f"  - {col}")

# ------------------------------------------------------------
# Coverage from summary file if available
# ------------------------------------------------------------

print("\nNORMALIZATION COVERAGE")
print("-" * 78)

if SUMMARY_FILE.exists():

    summary = pd.read_csv(SUMMARY_FILE)

    print(f"Summary File       : {SUMMARY_FILE.name}")
    print(f"Summary Rows       : {len(summary):,}")

    # Display useful coverage-related values
    coverage_cols = [
        c for c in summary.columns
        if any(x in c.lower()
               for x in ["coverage", "matched", "confidence"])
    ]

    if coverage_cols:
        for col in coverage_cols:
            values = summary[col].dropna()

            if len(values) > 0:
                print(f"{col:<28}: {values.iloc[-1]}")

else:
    print("Summary File       : Not found")

# ------------------------------------------------------------
# Sample normalized skills
# ------------------------------------------------------------

print("\nSAMPLE NORMALIZED SKILLS")
print("-" * 78)

display_cols = [
    c for c in df.columns
    if any(x in c.lower()
           for x in ["skill", "normalized", "canonical", "esco"])
]

if display_cols:
    print(df[display_cols].head(10).to_string(index=False))
else:
    print("Normalized skill columns could not be automatically identified.")

# ------------------------------------------------------------
# Methodology
# ------------------------------------------------------------

print("\nNORMALIZATION METHOD")
print("-" * 78)

print("1. Exact / dictionary matching")
print("2. Fuzzy string matching")
print("3. Semantic similarity matching")
print("4. ESCO taxonomy mapping")
print("5. Canonical skill assignment")

print("\nNormalization converts extracted skill variants into")
print("standardized skill concepts for reliable aggregation,")
print("feature engineering and role classification.")

print("\n" + "=" * 78)
print("SKILL NORMALIZATION EVIDENCE COMPLETE")
print("=" * 78)