from pathlib import Path
import joblib
import pandas as pd

print("=" * 78)
print("9.3 BEST MODEL – LOGISTIC REGRESSION")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

MODEL_FILE = ROOT / "models" / "best_model.pkl"
LABEL_FILE = ROOT / "models" / "label_encoder.pkl"
FEATURE_FILE = ROOT / "models" / "selected_feature_columns.pkl"
REPORT_FILE = ROOT / "reports" / "classification_report.txt"

# --------------------------------------------------------------
# Load final model artifacts
# --------------------------------------------------------------

model = joblib.load(MODEL_FILE)
label_encoder = joblib.load(LABEL_FILE)
selected_features = joblib.load(FEATURE_FILE)

print("\nFINAL MODEL ARTIFACT")
print("-" * 78)

print(f"Model File             : {MODEL_FILE.name}")
print(f"Model Type             : {type(model).__name__}")
print(f"Model Features         : {model.n_features_in_}")
print(f"Selected Features      : {len(selected_features)}")

print("\nTARGET CLASSES")
print("-" * 78)

for i, cls in enumerate(label_encoder.classes_, 1):
    print(f"{i}. {cls}")

print("\nMODEL CONFIGURATION")
print("-" * 78)

print("Algorithm              : Logistic Regression")
print("Maximum Iterations     : 1000")
print("Random State            : 42")
print("Feature Scaling        : StandardScaler")
print("Feature Selection      : VarianceThreshold")

# --------------------------------------------------------------
# Classification report
# --------------------------------------------------------------

print("\nCLASSIFICATION REPORT")
print("-" * 78)

if REPORT_FILE.exists():

    report_text = REPORT_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    # Display only the classification metrics section
    print(report_text.strip())

else:
    print("Classification report file not found.")

# --------------------------------------------------------------
# Final decision
# --------------------------------------------------------------

print("\nMODEL SELECTION DECISION")
print("-" * 78)

print("Selected Model         : Logistic Regression")
print("Reason                 : Highest overall project performance")
print("                        among evaluated classification models.")

print("\n" + "=" * 78)
print("9.3 BEST MODEL EVIDENCE COMPLETE")
print("=" * 78)