from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

print("=" * 80)
print("TRAIN / TEST SPLIT AUDIT")
print("=" * 80)

extensions = {
    ".py",
    ".ipynb"
}

keywords = [
    "train_test_split",
    "X_train",
    "X_test",
    "y_train",
    "y_test",
    "test_size",
    "train_size",
    "classification_report",
    "confusion_matrix",
]

found = False

for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    if path.suffix.lower() not in extensions:
        continue

    # Ignore virtual environments/cache folders
    if any(
        part in {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules"
        }
        for part in path.parts
    ):
        continue

    try:
        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        continue

    matched = []

    for keyword in keywords:

        if keyword in text:

            matched.append(keyword)

    if matched:

        found = True

        print()
        print("-" * 80)
        print("FILE:")
        print(path)
        print()
        print("MATCHED:")
        print(", ".join(matched))
        print()
        print("RELEVANT LINES:")
        print("-" * 80)

        lines = text.splitlines()

        for number, line in enumerate(lines, start=1):

            if any(
                keyword in line
                for keyword in keywords
            ):

                print(
                    f"{number:4}: {line}"
                )


print()

if not found:

    print(
        "NO TRAIN/TEST SPLIT IMPLEMENTATION FOUND."
    )

print()
print("=" * 80)
print("END OF AUDIT")
print("=" * 80)