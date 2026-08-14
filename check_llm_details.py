"""
=========================================================
VERIFY LLM EXTRACTION CONFIGURATION
AI-Powered Job Posting Analyzer
=========================================================
Run from project root:

python check_llm_details.py
=========================================================
"""

from pathlib import Path
import ast
import re


PROJECT_ROOT = Path(__file__).resolve().parent


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# =========================================================
# 1. FILE LOCATIONS
# =========================================================

print_section("1. EXTRACTION FILE LOCATIONS")

files_to_check = [
    PROJECT_ROOT / "src" / "config" / "settings.py",
    PROJECT_ROOT / "src" / "ai" / "clients" / "groq_client.py",
    PROJECT_ROOT / "src" / "ai" / "extraction" / "extractor.py",
    PROJECT_ROOT / "src" / "ai" / "prompts" / "skill_extraction_v1.txt",
    PROJECT_ROOT / "src" / "ai" / "prompts" / "prompt_loader.py",
    PROJECT_ROOT / "src" / "ai" / "validation" / "schema.py",
    PROJECT_ROOT / "src" / "ai" / "validation" / "validator.py",
]

for path in files_to_check:
    status = "FOUND" if path.exists() else "NOT FOUND"
    print(f"{status:12} : {path}")


# =========================================================
# 2. CURRENT MODEL SETTINGS
# =========================================================

print_section("2. CURRENT LLM SETTINGS")

settings_file = (
    PROJECT_ROOT
    / "src"
    / "config"
    / "settings.py"
)

if settings_file.exists():

    source = settings_file.read_text(
        encoding="utf-8"
    )

    print(source)

else:
    print("settings.py not found.")


# =========================================================
# 3. GROQ CLIENT CONFIGURATION
# =========================================================

print_section("3. GROQ CLIENT CONFIGURATION")

groq_file = (
    PROJECT_ROOT
    / "src"
    / "ai"
    / "clients"
    / "groq_client.py"
)

if groq_file.exists():

    source = groq_file.read_text(
        encoding="utf-8"
    )

    print(source)

else:
    print("groq_client.py not found.")


# =========================================================
# 4. CURRENT PROMPT
# =========================================================

print_section("4. CURRENT EXTRACTION PROMPT")

prompt_file = (
    PROJECT_ROOT
    / "src"
    / "ai"
    / "prompts"
    / "skill_extraction_v1.txt"
)

if prompt_file.exists():

    prompt = prompt_file.read_text(
        encoding="utf-8"
    )

    print(prompt)

else:
    print("skill_extraction_v1.txt not found.")


# =========================================================
# 5. PYDANTIC SCHEMA
# =========================================================

print_section("5. PYDANTIC EXTRACTION SCHEMA")

schema_file = (
    PROJECT_ROOT
    / "src"
    / "ai"
    / "validation"
    / "schema.py"
)

if schema_file.exists():

    print(
        schema_file.read_text(
            encoding="utf-8"
        )
    )

else:
    print("schema.py not found.")


# =========================================================
# 6. VALIDATOR
# =========================================================

print_section("6. OUTPUT VALIDATOR")

validator_file = (
    PROJECT_ROOT
    / "src"
    / "ai"
    / "validation"
    / "validator.py"
)

if validator_file.exists():

    print(
        validator_file.read_text(
            encoding="utf-8"
        )
    )

else:
    print("validator.py not found.")


# =========================================================
# 7. EXTRACTION ORCHESTRATOR
# =========================================================

print_section("7. SKILL EXTRACTOR")

extractor_file = (
    PROJECT_ROOT
    / "src"
    / "ai"
    / "extraction"
    / "extractor.py"
)

if extractor_file.exists():

    print(
        extractor_file.read_text(
            encoding="utf-8"
        )
    )

else:
    print("extractor.py not found.")


# =========================================================
# 8. CACHE IMPLEMENTATION
# =========================================================

print_section("8. CACHE IMPLEMENTATION")

cache_files = [
    PROJECT_ROOT / "src" / "ai" / "cache" / "cache_manager.py",
    PROJECT_ROOT / "src" / "ai" / "cache" / "cache_utils.py",
]

for cache_file in cache_files:

    print()
    print("-" * 70)
    print(cache_file)

    if cache_file.exists():

        print(
            cache_file.read_text(
                encoding="utf-8"
            )
        )

    else:

        print("NOT FOUND")


# =========================================================
# 9. HISTORICAL PHASE 5 EXTRACTION SCRIPTS
# =========================================================

print_section("9. HISTORICAL PHASE 5 EXTRACTION SCRIPTS")

phase5_files = list(
    PROJECT_ROOT.glob(
        "**/phase5_ai_skill_extraction*.py"
    )
)

if not phase5_files:

    print(
        "No phase5_ai_skill_extraction*.py "
        "files found inside project."
    )

else:

    for path in phase5_files:

        print()
        print("-" * 70)
        print(path)

        source = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        # Print model lines
        print("\nMODEL LINES:")
        for line in source.splitlines():
            if "model=" in line:
                print(line.strip())

        # Print temperature lines
        print("\nTEMPERATURE LINES:")
        for line in source.splitlines():
            if "temperature=" in line:
                print(line.strip())

        # Print max token lines
        print("\nMAX TOKEN LINES:")
        for line in source.splitlines():
            if "max_tokens" in line:
                print(line.strip())

        # Print retry lines
        print("\nRETRY LINES:")
        for line in source.splitlines():
            if (
                "MAX_RETRIES" in line
                or "retry" in line.lower()
            ):
                print(line.strip())

        # Print prompt-related section
        print("\nPROMPT-RELATED LINES:")

        lines = source.splitlines()

        for i, line in enumerate(lines):

            if "prompt" in line.lower():

                start = max(0, i - 2)
                end = min(
                    len(lines),
                    i + 12
                )

                print(
                    "\n".join(
                        lines[start:end]
                    )
                )


# =========================================================
# 10. DATASET USED FOR EXTRACTION
# =========================================================

print_section("10. EXTRACTION DATASET FILES")

dataset_files = [
    PROJECT_ROOT / "data" / "processed" / "sample_200.csv",
    PROJECT_ROOT / "data" / "processed" / "sample_200_with_ai_skills.csv",
]

for path in dataset_files:

    if path.exists():

        print(
            f"FOUND : {path}"
        )

        try:

            import pandas as pd

            df = pd.read_csv(path)

            print(
                f"Rows    : {len(df):,}"
            )

            print(
                f"Columns : {len(df.columns)}"
            )

            print(
                f"Column names:"
            )

            for column in df.columns:
                print(
                    f"  - {column}"
                )

        except Exception as e:

            print(
                f"Could not inspect CSV: {e}"
            )

    else:

        print(
            f"NOT FOUND : {path}"
        )


# =========================================================
# 11. FINAL INTERPRETATION CHECK
# =========================================================

print_section("11. IMPORTANT")

print(
    """
DO NOT PUT VALUES INTO THE REPORT YET.

We need to determine:

1. Which LLM model was used for the final extraction dataset.
2. Which exact prompt generated that dataset.
3. Temperature.
4. Max tokens.
5. Top-p, if configured.
6. Response format.
7. Retry behavior.
8. Cache behavior.
9. Validation behavior.
10. What happened when extraction failed.
11. Whether the older Phase 5 extractor or the newer
    modular SkillExtractor produced sample_200_with_ai_skills.csv.

Paste the COMPLETE TERMINAL OUTPUT back into ChatGPT.
"""
)