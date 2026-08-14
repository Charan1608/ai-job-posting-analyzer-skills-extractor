from pathlib import Path
import pandas as pd

print("=" * 78)
print("9.5 ROLE CLASSIFICATION – CONFUSION MATRIX")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "reports" / "confusion_matrix.csv"

if not FILE.exists():
    raise FileNotFoundError(
        f"Confusion matrix file not found:\n{FILE}"
    )

cm = pd.read_csv(FILE)

print("\nCONFUSION MATRIX")
print("-" * 78)

print(cm.to_string(index=False))

print("\nMATRIX INTERPRETATION")
print("-" * 78)

print("Rows    : Actual role")
print("Columns : Predicted role")
print("Diagonal values : Correct classifications")
print("Off-diagonal values : Misclassifications")

print("\nKEY OBSERVATIONS")
print("-" * 78)

# Extract class names
classes = list(cm.columns[1:])

for _, row in cm.iterrows():

    actual = row.iloc[0]

    # Exclude the actual-role column
    values = row.iloc[1:].astype(int)

    correct = int(values.loc[
        values.index == actual
    ].iloc[0]) if actual in values.index else 0

    errors = values.sum() - correct

    if errors > 0:
        top_prediction = values.drop(
            labels=[actual],
            errors="ignore"
        ).idxmax()

        top_count = int(
            values.drop(
                labels=[actual],
                errors="ignore"
            ).max()
        )

        print(
            f"{actual:<22} : "
            f"{correct} correct | "
            f"{errors} errors | "
            f"main confusion → "
            f"{top_prediction} ({top_count})"
        )

print("\n" + "=" * 78)
print("9.5 CONFUSION MATRIX EVIDENCE COMPLETE")
print("=" * 78)