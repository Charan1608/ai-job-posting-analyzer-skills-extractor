import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "job_postings.db"

print("=" * 70)
print("EXISTING SQLITE DATABASE INSPECTION")
print("=" * 70)

print(f"\nDatabase : {DB}")
print(f"Exists   : {DB.exists()}")

if not DB.exists():
    raise FileNotFoundError(f"Database not found: {DB}")

con = sqlite3.connect(DB)
cur = con.cursor()

tables = cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("\nTables:")
print("-" * 70)

if not tables:
    print("No tables found.")
else:
    for table in tables:
        print(f"- {table[0]}")

print("\nTable Row Counts:")
print("-" * 70)

for (table,) in tables:
    count = cur.execute(
        f'SELECT COUNT(*) FROM "{table}"'
    ).fetchone()[0]

    print(f"{table:<40} : {count:,}")

con.close()

print("\n" + "=" * 70)
print("SQLITE INSPECTION COMPLETE")
print("=" * 70)