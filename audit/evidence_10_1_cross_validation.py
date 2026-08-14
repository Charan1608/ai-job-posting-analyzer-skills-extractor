from pathlib import Path
import pandas as pd

print("=" * 78)
print("10.1 MODEL EVALUATION – CROSS-VALIDATION")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "reports" / "model_comparison.csv"

if not FILE.exists():
    raise FileNotFoundError(
        f"Model comparison file not found:\n{FILE}"
    )

df = pd.read_csv(FILE)

print("\nCROSS-VALIDATION CONFIGURATION")
print("-" * 78)

print("Validation Method      : Stratified K-Fold")
print("Number of Folds        : 5")
print("Shuffling              : Enabled")
print("Random State            : 42")
print("Evaluation Metrics     : Accuracy, Weighted F1")

print("\nCROSS-VALIDATION RESULTS")
print("-" * 78)

columns = [
    "Model",
    "CV_Accuracy_Mean",
    "CV_Accuracy_Std",
    "CV_F1_Weighted_Mean",
    "CV_F1_Weighted_Std",
]

available = [c for c in columns if c in df.columns]

result = df[available].copy()

for col in available:
    if col != "Model":
        result[col] = result[col].astype(float).round(4)

print(result.to_string(index=False))

print("\nBEST CROSS-VALIDATED MODEL")
print("-" * 78)

if "CV_F1_Weighted_Mean" in df.columns:

    best = df.loc[
        df["CV_F1_Weighted_Mean"].idxmax()
    ]

    print(f"Model                 : {best['Model']}")
    print(
        f"Mean CV Accuracy     : "
        f"{best['CV_Accuracy_Mean']:.4f}"
    )
    print(
        f"Accuracy Std. Dev.   : "
        f"{best['CV_Accuracy_Std']:.4f}"
    )
    print(
        f"Mean CV Weighted F1  : "
        f"{best['CV_F1_Weighted_Mean']:.4f}"
    )
    print(
        f"F1 Std. Dev.         : "
        f"{best['CV_F1_Weighted_Std']:.4f}"
    )

print("\nVALIDATION FLOW")
print("-" * 78)

print("Training Data")
print("      ↓")
print("Stratified 5-Fold Cross-Validation")
print("      ↓")
print("Accuracy + Weighted F1 per Fold")
print("      ↓")
print("Mean and Standard Deviation")
print("      ↓")
print("Model Generalization Assessment")

print("\n" + "=" * 78)
print("10.1 CROSS-VALIDATION EVIDENCE COMPLETE")
print("=" * 78)