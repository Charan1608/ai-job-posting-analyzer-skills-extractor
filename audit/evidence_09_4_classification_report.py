from pathlib import Path

print("=" * 78)
print("9.4 ROLE CLASSIFICATION – CLASSIFICATION REPORT")
print("=" * 78)

ROOT = Path(__file__).resolve().parents[1]

REPORT_FILE = ROOT / "reports" / "classification_report.txt"

if not REPORT_FILE.exists():
    raise FileNotFoundError(
        f"Classification report not found:\n{REPORT_FILE}"
    )

text = REPORT_FILE.read_text(
    encoding="utf-8",
    errors="ignore"
).strip()

print("\nFINAL CLASSIFICATION PERFORMANCE")
print("-" * 78)

print(text)

print("\n" + "=" * 78)
print("9.4 CLASSIFICATION REPORT EVIDENCE COMPLETE")
print("=" * 78)