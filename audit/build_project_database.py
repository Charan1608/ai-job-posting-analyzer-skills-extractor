from pathlib import Path
import duckdb
import re
import time
from datetime import datetime


# ============================================================
# AI-POWERED JOB POSTING ANALYZER
# CENTRAL PROJECT DATABASE BUILDER
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

STORAGE_DIR = ROOT / "storage"
DB_FILE = STORAGE_DIR / "ai_job_posting_analyzer.duckdb"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("AI-POWERED JOB POSTING ANALYZER")
print("CENTRAL PROJECT DATABASE BUILDER")
print("=" * 80)

print(f"\nProject Root : {ROOT}")
print(f"Database     : {DB_FILE}")


# ============================================================
# CONNECT
# ============================================================

con = duckdb.connect(str(DB_FILE))


# ============================================================
# PROJECT METADATA
# ============================================================

con.execute("""
CREATE OR REPLACE TABLE project_metadata (
    key VARCHAR,
    value VARCHAR
)
""")

metadata = [
    ("project_name",
     "AI-Powered Job Posting Analyzer & Skills Extractor"),

    ("dataset",
     "LinkedIn Job Postings Dataset (2023-2024)"),

    ("source",
     "Kaggle"),

    ("analytical_sample",
     "Final 200 job postings"),

    ("database_engine",
     "DuckDB"),

    ("purpose",
     "Central analytical data storage"),

    ("pipeline",
     "Raw Data -> Cleaning -> Skill Extraction -> Normalization -> ML -> Evaluation -> Dashboard"),
]

for key, value in metadata:
    con.execute(
        "INSERT INTO project_metadata VALUES (?, ?)",
        [key, value]
    )


# ============================================================
# FILE CATALOG
# ============================================================

print("\nCreating project file catalog...")

con.execute("""
CREATE OR REPLACE TABLE project_files (
    relative_path VARCHAR,
    file_name VARCHAR,
    extension VARCHAR,
    directory VARCHAR,
    file_size_mb DOUBLE,
    modified_time TIMESTAMP
)
""")

all_files = [
    p for p in ROOT.rglob("*")
    if p.is_file()
    and ".git" not in p.parts
    and "__pycache__" not in p.parts
    and p != DB_FILE
]

for path in all_files:

    relative = path.relative_to(ROOT)

    modified_time = datetime.fromtimestamp(
        path.stat().st_mtime
    )

    con.execute(
        """
        INSERT INTO project_files
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            str(relative),
            path.name,
            path.suffix.lower(),
            str(relative.parent),
            round(path.stat().st_size / (1024 * 1024), 3),
            modified_time,
        ]
    )

print(f"Project files catalogued : {len(all_files):,}")


# ============================================================
# TABLE NAME CLEANING
# ============================================================

def safe_table_name(name):

    name = name.lower()

    name = re.sub(
        r"[^a-z0-9_]+",
        "_",
        name
    )

    name = re.sub(
        r"_+",
        "_",
        name
    )

    name = name.strip("_")

    if not name:
        name = "unnamed_table"

    return name


# ============================================================
# CSV IMPORT
# ============================================================

def import_csv(csv_path, table_name):

    print("\nImporting CSV")
    print("-" * 70)

    print(f"File  : {csv_path.relative_to(ROOT)}")
    print(f"Table : {table_name}")

    start = time.perf_counter()

    con.execute(
        f"""
        CREATE OR REPLACE TABLE "{table_name}" AS
        SELECT *
        FROM read_csv_auto(
            '{csv_path.as_posix()}',
            header = true,
            ignore_errors = true
        )
        """
    )

    count = con.execute(
        f'SELECT COUNT(*) FROM "{table_name}"'
    ).fetchone()[0]

    elapsed = time.perf_counter() - start

    print(f"Rows  : {count:,}")
    print(f"Time  : {elapsed:.2f} seconds")

    return count


# ============================================================
# PROCESSED DATA
# ============================================================

print("\n" + "=" * 80)
print("IMPORTING PROCESSED DATA")
print("=" * 80)

processed_dir = ROOT / "data" / "processed"

processed_files = sorted(
    processed_dir.glob("*.csv")
)

processed_count = 0

for csv_file in processed_files:

    table = safe_table_name(csv_file.stem)

    if table in {
        "project_metadata",
        "project_files",
        "database_inventory",
    }:
        table = "data_" + table

    try:

        import_csv(
            csv_file,
            table
        )

        processed_count += 1

    except Exception as e:

        print("\nWARNING")
        print(f"Could not import: {csv_file.name}")
        print(f"Reason: {e}")


# ============================================================
# REPORT CSV FILES
# ============================================================

print("\n" + "=" * 80)
print("IMPORTING REPORT DATA")
print("=" * 80)

reports_dir = ROOT / "reports"

report_files = sorted(
    reports_dir.rglob("*.csv")
)

report_count = 0

for csv_file in report_files:

    relative = csv_file.relative_to(ROOT)

    parts = list(relative.parts)

    parent_parts = [
        p.lower()
        for p in parts[:-1]
        if p.lower() != "reports"
    ]

    prefix_parts = []

    for p in parent_parts:

        cleaned = safe_table_name(p)

        if cleaned:
            prefix_parts.append(cleaned)

    prefix = "_".join(prefix_parts)

    base = safe_table_name(csv_file.stem)

    if prefix:
        table = f"report_{prefix}_{base}"
    else:
        table = f"report_{base}"

    table = safe_table_name(table)

    try:

        import_csv(
            csv_file,
            table
        )

        report_count += 1

    except Exception as e:

        print("\nWARNING")
        print(f"Could not import: {csv_file}")
        print(f"Reason: {e}")


# ============================================================
# RAW LINKEDIN DATASET
# ============================================================

print("\n" + "=" * 80)
print("RAW LINKEDIN DATASET")
print("=" * 80)

raw_candidates = [
    ROOT / "data" / "raw" / "postings.csv",
    ROOT / "data" / "raw" / "job_postings.csv",
]

raw_postings = None

for candidate in raw_candidates:

    if candidate.exists():
        raw_postings = candidate
        break


if raw_postings is not None:

    size_mb = raw_postings.stat().st_size / (
        1024 * 1024
    )

    print(
        f"\nRaw dataset found:"
        f"\n{raw_postings}"
    )

    print(
        f"\nApproximate size: "
        f"{size_mb:,.2f} MB"
    )

    answer = input(
        "\nImport complete raw dataset into DuckDB? [Y/N]: "
    ).strip().upper()

    if answer == "Y":

        try:

            import_csv(
                raw_postings,
                "raw_postings"
            )

        except Exception as e:

            print("\nRAW DATA IMPORT FAILED")
            print(e)

    else:

        print(
            "\nRaw CSV retained as original source artifact."
        )

else:

    print(
        "\nRaw postings CSV was not found."
    )


# ============================================================
# DATABASE INVENTORY
# ============================================================

print("\n" + "=" * 80)
print("DATABASE INVENTORY")
print("=" * 80)

con.execute("""
CREATE OR REPLACE TABLE database_inventory AS
SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema NOT IN (
    'information_schema',
    'pg_catalog'
)
ORDER BY table_name
""")


tables = con.execute("""
SELECT table_name
FROM database_inventory
ORDER BY table_name
""").fetchall()


print(
    f"\nTotal database tables : {len(tables):,}"
)


for (table,) in tables:

    try:

        count = con.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]

        print(
            f"{table:<65} "
            f"{count:>12,} rows"
        )

    except Exception:

        print(
            f"{table:<65} "
            f"[metadata]"
        )


# ============================================================
# CORE PROJECT TABLES
# ============================================================

print("\n" + "=" * 80)
print("CORE PROJECT DATA")
print("=" * 80)

core_tables = [
    "raw_postings",
    "cleaned_postings",
    "normalized_jobs",
    "normalized_skills_long",
    "ground_truth_normalized_skills_long",
    "final_ml_dataset_v2",
    "evaluation_per_job",
    "evaluation_summary",
    "normalization_quality",
    "normalization_summary",
    "skill_frequency",
    "skill_category_frequency",
    "skill_pairs",
    "company_skill_frequency",
    "location_skill_frequency",
    "top_false_positives",
    "top_false_negatives",
    "model_comparison",
    "confusion_matrix",
]


for table in core_tables:

    exists = con.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = ?
        """,
        [table]
    ).fetchone()[0]

    if exists:

        count = con.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]

        print(
            f"{table:<45} : "
            f"{count:,} rows"
        )


# ============================================================
# FINAL DATABASE STATISTICS
# ============================================================

print("\n" + "=" * 80)
print("FINAL DATABASE STATISTICS")
print("=" * 80)

database_size_mb = (
    DB_FILE.stat().st_size /
    (1024 * 1024)
    if DB_FILE.exists()
    else 0
)

print(
    f"\nProcessed CSV files imported : "
    f"{processed_count}"
)

print(
    f"Report CSV files imported    : "
    f"{report_count}"
)

print(
    f"Database size                 : "
    f"{database_size_mb:,.2f} MB"
)


# ============================================================
# CHECKPOINT AND CLOSE
# ============================================================

con.execute("CHECKPOINT")
con.close()


print("\n" + "=" * 80)
print("DATABASE BUILD COMPLETE")
print("=" * 80)

print(
    f"\nCentral database:"
    f"\n{DB_FILE}"
)

print("\nStorage layer contains:")
print("  1. Project metadata")
print("  2. Complete project file catalog")
print("  3. Raw dataset (if imported)")
print("  4. Processed datasets")
print("  5. Normalization outputs")
print("  6. Evaluation outputs")
print("  7. Machine-learning datasets")
print("  8. Model comparison outputs")
print("  9. Report CSV outputs")

print(
    "\nSource code, trained models, images, "
    "and Power BI files remain in their "
    "original project directories."
)

print("\nREADY FOR DATABASE EVIDENCE SCREENSHOT.")
print("=" * 80)