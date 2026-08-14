from pathlib import Path
import pandas as pd

print("=" * 78)
print("9.6 ROLE CLASSIFICATION – ERROR / MISCLASSIFICATION ANALYSIS")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "reports" / "misclassification_examples.csv"

if not FILE.exists():
    raise FileNotFoundError(
        f"Misclassification file not found:\n{FILE}"
    )

df = pd.read_csv(FILE)

print("\nMISCLASSIFICATION SUMMARY")
print("-" * 78)

total_errors = len(df)

print(f"Misclassified Test Records : {total_errors}")
print(f"Correct Test Records       : {40 - total_errors}")
print(f"Test Records               : 40")
print(f"Test Accuracy              : {((40-total_errors)/40)*100:.2f}%")

print("\nMISCLASSIFICATION PAIRS")
print("-" * 78)

pairs = (
    df.groupby(
        ["actual_role", "predicted_role"]
    )
    .size()
    .sort_values(ascending=False)
)

for (actual, predicted), count in pairs.items():
    print(
        f"{actual} -> {predicted} : {count}"
    )

print("\nTOP MISCLASSIFIED CASES")
print("-" * 78)

display_columns = [
    "job_id",
    "title",
    "actual_role",
    "predicted_role",
]

available = [
    c for c in display_columns
    if c in df.columns
]

print(
    df[available]
    .head(10)
    .to_string(index=False)
)

print("\nERROR ANALYSIS")
print("-" * 78)

print(
    "The principal classification errors occur between roles "
    "with overlapping analytical, technical and business-oriented "
    "skill requirements."
)

print("\nKEY CONFUSION AREAS")
print("-" * 78)

for (actual, predicted), count in pairs.head(5).items():
    print(
        f"• {actual} → {predicted}: {count} case(s)"
    )

print("\n" + "=" * 78)
print("9.6 MISCLASSIFICATION ANALYSIS EVIDENCE COMPLETE")
print("=" * 78)