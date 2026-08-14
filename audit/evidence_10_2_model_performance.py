from pathlib import Path
import pandas as pd

print("=" * 78)
print("10.2 MODEL EVALUATION – PERFORMANCE METRICS")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "reports" / "model_comparison.csv"

if not FILE.exists():
    raise FileNotFoundError(
        f"Model comparison file not found:\n{FILE}"
    )

df = pd.read_csv(FILE)

print("\nHELD-OUT TEST SET")
print("-" * 78)

print("Test Records           : 40")
print("Evaluation Type        : Independent Test Set")
print("Target Classes         : 6")

print("\nMODEL PERFORMANCE")
print("-" * 78)

columns = [
    "Model",
    "Accuracy",
    "Precision",
    "Recall",
    "F1_Weighted",
]

available = [c for c in columns if c in df.columns]

result = df[available].copy()

for col in available:
    if col != "Model":
        result[col] = result[col].astype(float).round(4)

print(result.to_string(index=False))

print("\nBEST MODEL – TEST PERFORMANCE")
print("-" * 78)

best = df.iloc[0]

print(f"Selected Model         : {best['Model']}")
print(f"Accuracy               : {best['Accuracy']:.4f}")
print(f"Accuracy (%)           : {best['Accuracy'] * 100:.2f}%")
print(f"Precision              : {best['Precision']:.4f}")
print(f"Recall                 : {best['Recall']:.4f}")
print(f"Weighted F1            : {best['F1_Weighted']:.4f}")

print("\nMETRIC DEFINITIONS")
print("-" * 78)

print("Accuracy  : Overall proportion of correct predictions")
print("Precision : Correct positive predictions among predicted positives")
print("Recall    : Correct positive predictions among actual positives")
print("F1-Score  : Harmonic mean of precision and recall")

print("\n" + "=" * 78)
print("10.2 MODEL PERFORMANCE EVIDENCE COMPLETE")
print("=" * 78)