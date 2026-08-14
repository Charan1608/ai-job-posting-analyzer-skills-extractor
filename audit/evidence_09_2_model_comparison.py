from pathlib import Path
import pandas as pd

print("=" * 78)
print("9.2 ROLE CLASSIFICATION – MODEL COMPARISON")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "reports" / "model_comparison.csv"

if not FILE.exists():
    raise FileNotFoundError(f"Model comparison file not found:\n{FILE}")

df = pd.read_csv(FILE)

print("\nMODEL EVALUATION RESULTS")
print("-" * 78)

display_columns = [
    "Model",
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Weighted",
    "CV_Accuracy_Mean",
    "CV_F1_Weighted_Mean",
]

available = [c for c in display_columns if c in df.columns]

result = df[available].copy()

for col in available:
    if col != "Model":
        result[col] = result[col].astype(float).round(4)

print(result.to_string(index=False))

print("\nMODEL RANKING")
print("-" * 78)

if "CV_F1_Weighted_Mean" in df.columns:
    ranking = df.sort_values(
        "CV_F1_Weighted_Mean",
        ascending=False
    )

    for i, (_, row) in enumerate(ranking.iterrows(), 1):
        print(
            f"{i}. {row['Model']:<22} "
            f"CV F1 = {row['CV_F1_Weighted_Mean']:.4f}"
        )

print("\nBEST MODEL")
print("-" * 78)

best = df.iloc[0]

print(f"Model                 : {best['Model']}")
print(f"Test Accuracy         : {best['Accuracy']:.4f}")
print(f"Test Precision        : {best['Precision']:.4f}")
print(f"Test Recall           : {best['Recall']:.4f}")
print(f"Test Weighted F1      : {best['F1_Weighted']:.4f}")

if "CV_Accuracy_Mean" in df.columns:
    print(f"CV Accuracy           : {best['CV_Accuracy_Mean']:.4f}")

if "CV_F1_Weighted_Mean" in df.columns:
    print(f"CV Weighted F1        : {best['CV_F1_Weighted_Mean']:.4f}")

print("\n" + "=" * 78)
print("9.2 MODEL COMPARISON EVIDENCE COMPLETE")
print("=" * 78)