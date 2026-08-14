from pathlib import Path
import pandas as pd
import joblib

# ==============================================================
# 8.1 FEATURE ENGINEERING – SKILL-BASED FEATURE CONSTRUCTION
# ==============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "final_ml_dataset_v2.csv"
FEATURE_FILE = ROOT / "data" / "processed" / "feature_engineered_jobs_v2.csv"
SELECTED_FILE = ROOT / "models" / "selected_feature_columns.pkl"
SELECTOR_FILE = ROOT / "models" / "variance_selector.pkl"

print("=" * 78)
print("8.1 FEATURE ENGINEERING – SKILL-BASED FEATURE CONSTRUCTION")
print("=" * 78)

# --------------------------------------------------------------
# Load final ML dataset
# --------------------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Final ML dataset not found:\n{DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

print("\nFINAL ML DATASET")
print("-" * 78)

print(f"Dataset File          : {DATA_FILE.name}")
print(f"Records               : {len(df):,}")
print(f"Total Columns         : {len(df.columns):,}")

# --------------------------------------------------------------
# Identify target and metadata
# --------------------------------------------------------------

metadata_columns = [
    "job_id",
    "company_name",
    "title",
    "location",
    "experience",
    "education",
    "work_type",
    "standard_title",
]

existing_metadata = [
    c for c in metadata_columns
    if c in df.columns
]

feature_columns = [
    c for c in df.columns
    if c not in existing_metadata
]

print(f"Metadata Columns      : {len(existing_metadata)}")
print(f"Feature Columns       : {len(feature_columns)}")

# --------------------------------------------------------------
# Feature categories
# --------------------------------------------------------------

feature_groups = {
    "Skill Count / Diversity": [
        "total_skills",
        "skill_diversity",
    ],

    "Skill Category Features": [
        "programming_languages",
        "databases",
        "bi_tools",
        "cloud_tools",
        "ml_skills",
        "ai_skills",
        "big_data",
        "data_engineering",
        "devops",
        "version_control",
        "etl_tools",
        "spreadsheet",
        "analytics",
        "business_analysis",
    ],

    "Domain Scores": [
        "analytics_score",
        "data_engineering_score",
        "ai_readiness_score",
        "cloud_score",
        "visualization_score",
    ],
}

print("\nENGINEERED FEATURE GROUPS")
print("-" * 78)

for group, columns in feature_groups.items():

    available = [
        c for c in columns
        if c in df.columns
    ]

    print(
        f"{group:<28}: "
        f"{len(available)} features"
    )

# --------------------------------------------------------------
# Binary skill indicators
# --------------------------------------------------------------

binary_features = [
    c for c in feature_columns
    if c.startswith("has_")
]

print("\nSKILL PRESENCE INDICATORS")
print("-" * 78)

print(f"Binary Skill Indicators : {len(binary_features)}")

if binary_features:
    print("\nSample Indicators:")
    for feature in binary_features[:15]:
        print(f"  • {feature}")

# --------------------------------------------------------------
# Load final feature-selection artifacts
# --------------------------------------------------------------

print("\nFEATURE SELECTION ARTIFACTS")
print("-" * 78)

if SELECTED_FILE.exists():

    selected_features = joblib.load(
        SELECTED_FILE
    )

    print(
        f"Selected Features      : "
        f"{len(selected_features)}"
    )

else:
    selected_features = []
    print("Selected feature artifact: NOT FOUND")

if SELECTOR_FILE.exists():

    selector = joblib.load(
        SELECTOR_FILE
    )

    print(
        f"Variance Selector Output: "
        f"{selector.get_support().sum()}"
    )

else:
    selector = None
    print("Variance selector       : NOT FOUND")

# --------------------------------------------------------------
# Feature-selection summary
# --------------------------------------------------------------

print("\nFEATURE ENGINEERING FLOW")
print("-" * 78)

print("Normalized Skills")
print("        ↓")
print("Skill Category Features")
print("        ↓")
print("Skill Count / Diversity Features")
print("        ↓")
print("Domain-Specific Scores")
print("        ↓")
print("Binary Skill Presence Indicators")
print("        ↓")
print("Final ML Feature Matrix")
print("        ↓")
print("Variance-Based Feature Selection")
print("        ↓")
print("Selected Features for Classification")

# --------------------------------------------------------------
# Sample feature values
# --------------------------------------------------------------

print("\nSAMPLE ENGINEERED FEATURES")
print("-" * 78)

sample_features = [
    "total_skills",
    "programming_languages",
    "databases",
    "bi_tools",
    "cloud_tools",
    "ml_skills",
    "analytics",
    "business_analysis",
    "skill_diversity",
    "analytics_score",
    "data_engineering_score",
    "ai_readiness_score",
    "cloud_score",
    "visualization_score",
]

available_sample = [
    c for c in sample_features
    if c in df.columns
]

if available_sample:

    sample = df[available_sample].head(3)

    print(sample.to_string(index=False))

# --------------------------------------------------------------
# Final summary
# --------------------------------------------------------------

print("\nFEATURE ENGINEERING SUMMARY")
print("-" * 78)

print(f"Input Records          : {len(df):,}")
print(f"Input Columns          : {len(df.columns):,}")
print(f"Model Features         : {len(feature_columns):,}")

if selected_features:
    print(
        f"Selected Model Features: "
        f"{len(selected_features):,}"
    )

print("\n" + "=" * 78)
print("8.1 FEATURE ENGINEERING EVIDENCE COMPLETE")
print("=" * 78)