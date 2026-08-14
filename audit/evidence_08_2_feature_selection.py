from pathlib import Path
import joblib
import pandas as pd

print("=" * 78)
print("8.2 FEATURE SELECTION – FINAL ML FEATURE MATRIX")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "final_ml_dataset_v2.csv"
SELECTED_FILE = ROOT / "models" / "selected_feature_columns.pkl"
SELECTOR_FILE = ROOT / "models" / "variance_selector.pkl"

# --------------------------------------------------------------
# Load artifacts
# --------------------------------------------------------------

df = pd.read_csv(DATA_FILE)
selected_features = joblib.load(SELECTED_FILE)
selector = joblib.load(SELECTOR_FILE)

print("\nFEATURE SELECTION INPUT")
print("-" * 78)

print(f"Dataset                 : {DATA_FILE.name}")
print(f"Records                 : {len(df):,}")
print(f"Initial Feature Count   : {len(df.columns):,}")

# --------------------------------------------------------------
# Selection information
# --------------------------------------------------------------

raw_feature_count = len(
    [c for c in df.columns if c != "standard_title"]
)

selected_count = len(selected_features)
selector_count = int(selector.get_support().sum())

print("\nVARIANCE-BASED FEATURE SELECTION")
print("-" * 78)

print(f"Features Before Selection : {raw_feature_count}")
print(f"Features After Selection  : {selector_count}")
print(f"Saved Selected Features   : {selected_count}")

print(
    f"Feature Reduction         : "
    f"{raw_feature_count - selected_count}"
)

reduction_pct = (
    (raw_feature_count - selected_count)
    / raw_feature_count * 100
)

print(f"Reduction Percentage      : {reduction_pct:.2f}%")

# --------------------------------------------------------------
# Selected feature categories
# --------------------------------------------------------------

print("\nSELECTED FEATURE GROUPS")
print("-" * 78)

groups = {
    "Core Skill Features": [
        "total_skills",
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

    "Skill / Domain Scores": [
        "skill_diversity",
        "analytics_score",
        "data_engineering_score",
        "ai_readiness_score",
        "cloud_score",
        "visualization_score",
    ],
}

for group, candidates in groups.items():
    available = [x for x in candidates if x in selected_features]
    print(f"{group:<28}: {len(available)}")

binary = [
    x for x in selected_features
    if str(x).startswith("has_")
]

print(f"{'Binary Skill Indicators':<28}: {len(binary)}")

# --------------------------------------------------------------
# Sample selected features
# --------------------------------------------------------------

print("\nSELECTED FEATURES")
print("-" * 78)

for i, feature in enumerate(selected_features, 1):
    print(f"{i:02d}. {feature}")

# --------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------

print("\nFEATURE SELECTION PIPELINE")
print("-" * 78)

print("Engineered Feature Matrix")
print("          ↓")
print("VarianceThreshold")
print("          ↓")
print("Low-Variance Features Removed")
print("          ↓")
print("Selected Feature Matrix")
print("          ↓")
print("StandardScaler")
print("          ↓")
print("Machine Learning Models")

print("\n" + "=" * 78)
print("8.2 FEATURE SELECTION EVIDENCE COMPLETE")
print("=" * 78)