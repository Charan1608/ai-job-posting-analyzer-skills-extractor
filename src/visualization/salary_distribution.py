from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 70)
print("SALARY DISTRIBUTION")
print("=" * 70)

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_file = Path("data/interim/business_analytics_postings.csv")
report_folder = Path("reports/eda")

report_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

df = pd.read_csv(input_file)

# -------------------------------------------------
# Find Salary Column
# -------------------------------------------------

salary_column = None

for col in [
    "med_salary",
    "max_salary",
    "min_salary",
    "normalized_salary"
]:
    if col in df.columns:
        if df[col].notna().sum() > 0:
            salary_column = col
            break

if salary_column is None:
    print("No salary column available.")
    exit()

# -------------------------------------------------
# Clean
# -------------------------------------------------

salary = df[salary_column].dropna()

salary = salary[
    (salary > 1000) &
    (salary < 500000)
]

print(f"Using column : {salary_column}")
print(f"Records : {len(salary)}")

# -------------------------------------------------
# Statistics
# -------------------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Average Salary",
        "Median Salary",
        "Minimum Salary",
        "Maximum Salary"
    ],
    "Value": [
        salary.mean(),
        salary.median(),
        salary.min(),
        salary.max()
    ]
})

print(summary)

summary.to_csv(
    report_folder / "salary_summary.csv",
    index=False
)

# -------------------------------------------------
# Histogram
# -------------------------------------------------

plt.figure(figsize=(10,6))

plt.hist(
    salary,
    bins=30
)

plt.title("Salary Distribution")

plt.xlabel("Salary")

plt.ylabel("Number of Job Postings")

plt.tight_layout()

plt.savefig(
    report_folder / "salary_distribution.png",
    dpi=300
)

plt.close()

print("\nReport Saved Successfully")

print(report_folder / "salary_summary.csv")
print(report_folder / "salary_distribution.png")