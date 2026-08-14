"""
=========================================================
Dataset Audit Module
Project : AI-Powered Job Posting Analyzer
Author  : Charan N
Purpose : Audit all raw datasets before preprocessing
=========================================================
"""

from pathlib import Path
import pandas as pd


def get_project_root():
    """
    Returns the project root directory.
    """
    return Path(__file__).resolve().parents[2]


def audit_csv(file_path: Path):
    """
    Reads a CSV file and returns audit information.
    """

    try:
        df = pd.read_csv(file_path)

        return {
            "File Name": file_path.name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum()),
            "Memory (MB)": round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2),
            "Status": "Success"
        }

    except Exception as e:

        return {
            "File Name": file_path.name,
            "Rows": "-",
            "Columns": "-",
            "Missing Values": "-",
            "Duplicate Rows": "-",
            "Memory (MB)": "-",
            "Status": f"Error : {e}"
        }


def main():

    print("=" * 70)
    print("AI-Powered Job Posting Analyzer")
    print("DATASET AUDIT")
    print("=" * 70)

    project_root = get_project_root()

    raw_folder = project_root / "data" / "raw"

    report_folder = project_root / "reports" / "audit"

    report_folder.mkdir(parents=True, exist_ok=True)

    csv_files = list(raw_folder.rglob("*.csv"))

    print(f"\nCSV Files Found : {len(csv_files)}")

    audit_results = []

    for file in csv_files:

        print(f"Reading : {file.name}")

        audit_results.append(audit_csv(file))

    audit_df = pd.DataFrame(audit_results)

    output_file = report_folder / "dataset_inventory.csv"

    audit_df.to_csv(output_file, index=False)

    print("\nAudit Summary\n")

    print(audit_df)

    print("\nReport Saved Successfully")

    print(output_file)


if __name__ == "__main__":
    main()