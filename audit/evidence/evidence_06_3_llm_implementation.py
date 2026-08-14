from pathlib import Path
import re
import json

# ================================================================
# 4B.3 LLM IMPLEMENTATION — COMPLETE CLIENT FEEDBACK EVIDENCE
# ================================================================

ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    ROOT
    / "audit"
    / "evidence"
    / "outputs"
    / "06_llm_implementation"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TXT_OUTPUT = OUTPUT_DIR / "04B_3_LLM_IMPLEMENTATION_EVIDENCE.txt"
JSON_OUTPUT = OUTPUT_DIR / "04B_3_LLM_IMPLEMENTATION_EVIDENCE.json"

print("=" * 90)
print("4B.3 LLM-BASED SKILL EXTRACTION")
print("COMPLETE CLIENT FEEDBACK EVIDENCE")
print("=" * 90)

print(f"\nProject root:\n{ROOT}")
print(f"\nOutput directory:\n{OUTPUT_DIR}")

# ----------------------------------------------------------------
# Locate likely project files
# ----------------------------------------------------------------

SEARCH_DIRS = [
    ROOT / "audit",
    ROOT / "app",
    ROOT / "src",
    ROOT / "scripts",
    ROOT / "pipeline",
    ROOT / "config",
]

files = []

for folder in SEARCH_DIRS:
    if folder.exists():
        files.extend(folder.rglob("*.py"))
        files.extend(folder.rglob("*.json"))
        files.extend(folder.rglob("*.txt"))
        files.extend(folder.rglob("*.yaml"))
        files.extend(folder.rglob("*.yml"))

files = sorted(set(files))

print(f"\nFiles scanned: {len(files)}")

# ----------------------------------------------------------------
# Read source files
# ----------------------------------------------------------------

source_text = {}

for file in files:
    try:
        source_text[str(file.relative_to(ROOT))] = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        pass


# ----------------------------------------------------------------
# Helper
# ----------------------------------------------------------------

def find_context(patterns, window=500):
    results = []

    for filename, text in source_text.items():

        for pattern in patterns:

            for match in re.finditer(
                pattern,
                text,
                flags=re.IGNORECASE | re.MULTILINE
            ):

                start = max(0, match.start() - window)
                end = min(len(text), match.end() + window)

                context = text[start:end].strip()

                results.append({
                    "file": filename,
                    "matched": match.group(0),
                    "context": context
                })

    return results


# ================================================================
# REQUIREMENT 1 — LLM USED
# ================================================================

llm_results = find_context([
    r"MODEL_NAME\s*=",
    r"model\s*=",
    r"model_name\s*=",
    r"llama[-\w.]+",
    r"Groq\s*\(",
    r"groq"
])


# ================================================================
# REQUIREMENT 2 — PROMPT
# ================================================================

prompt_results = find_context([
    r"SYSTEM_PROMPT",
    r"system_prompt",
    r"EXTRACTION_PROMPT",
    r"extraction_prompt",
    r"prompt\s*=",
    r"You are .*skill",
    r"extract .*skill",
])


# ================================================================
# REQUIREMENT 3 — JSON / SCHEMA
# ================================================================

schema_results = find_context([
    r"response_format",
    r"json_object",
    r"json_schema",
    r"json\.loads",
    r"json\.dumps",
    r"BaseModel",
    r"pydantic",
    r"schema",
    r"technical_skills",
    r"soft_skills",
    r"skills"
])


# ================================================================
# REQUIREMENT 4 — MODEL SETTINGS
# ================================================================

settings_results = find_context([
    r"temperature\s*=",
    r"max_tokens\s*=",
    r"max_completion_tokens\s*=",
    r"top_p\s*=",
    r"seed\s*=",
])


# ================================================================
# REQUIREMENT 5 — COST / RATE LIMIT
# ================================================================

rate_results = find_context([
    r"rate.?limit",
    r"quota",
    r"429",
    r"Too Many Requests",
    r"sleep\s*\(",
    r"time\.sleep",
    r"batch",
    r"batch_size",
    r"API",
])


# ================================================================
# REQUIREMENT 6 — CACHE
# ================================================================

cache_results = find_context([
    r"cache",
    r"cached",
    r"CACHE_FILE",
    r"cache_file",
    r"job_id.*cache",
    r"save.*cache",
    r"load.*cache",
])


# ================================================================
# REQUIREMENT 7 — FALLBACK / RETRY
# ================================================================

fallback_results = find_context([
    r"retry",
    r"Retry",
    r"backoff",
    r"exponential",
    r"fallback",
    r"Fallback",
    r"except\s+Exception",
    r"except\s+",
])


# ================================================================
# REQUIREMENT 8 — VALIDATION
# ================================================================

validation_results = find_context([
    r"validate",
    r"validation",
    r"ValidationError",
    r"json\.loads",
    r"schema",
    r"required",
    r"missing",
    r"invalid",
    r"None",
])


# ================================================================
# DATASET / EXTRACTION OUTPUT EVIDENCE
# ================================================================

data_results = find_context([
    r"sample_200",
    r"200",
    r"job_id",
    r"skills",
    r"extracted",
    r"normalized",
])


# ================================================================
# Build complete evidence structure
# ================================================================

evidence = {

    "project": {
        "project_root": str(ROOT),
        "files_scanned": len(files),
    },

    "client_requirements": {

        "1_llm_used": {
            "requirement":
                "Name the LLM used for extraction.",
            "evidence": llm_results,
        },

        "2_prompt": {
            "requirement":
                "Document the actual extraction prompt/instruction.",
            "evidence": prompt_results,
        },

        "3_json_schema": {
            "requirement":
                "Document the structured JSON output/schema.",
            "evidence": schema_results,
        },

        "4_model_settings": {
            "requirement":
                "Document temperature, token limits and other settings.",
            "evidence": settings_results,
        },

        "5_cost_rate_limit": {
            "requirement":
                "Document API cost/rate-limit handling.",
            "evidence": rate_results,
        },

        "6_caching": {
            "requirement":
                "Document extraction caching and reuse.",
            "evidence": cache_results,
        },

        "7_fallback_behavior": {
            "requirement":
                "Document retry/fallback/error handling.",
            "evidence": fallback_results,
        },

        "8_extraction_validation": {
            "requirement":
                "Document JSON/schema and output validation.",
            "evidence": validation_results,
        },
    },

    "data_extraction_evidence": data_results,
}


# ================================================================
# Human-readable report
# ================================================================

with open(TXT_OUTPUT, "w", encoding="utf-8") as f:

    f.write("=" * 90 + "\n")
    f.write("CHAPTER 4B.3 — LLM-BASED SKILL EXTRACTION\n")
    f.write("COMPLETE CLIENT FEEDBACK EVIDENCE\n")
    f.write("=" * 90 + "\n\n")

    f.write(f"PROJECT ROOT:\n{ROOT}\n\n")
    f.write(f"FILES SCANNED: {len(files)}\n\n")

    requirements = [
        ("1. LLM USED", "1_llm_used"),
        ("2. PROMPT", "2_prompt"),
        ("3. JSON / SCHEMA", "3_json_schema"),
        ("4. MODEL SETTINGS", "4_model_settings"),
        ("5. COST / RATE-LIMIT MANAGEMENT", "5_cost_rate_limit"),
        ("6. CACHING STRATEGY", "6_caching"),
        ("7. FALLBACK / RETRY BEHAVIOR", "7_fallback_behavior"),
        ("8. EXTRACTION VALIDATION", "8_extraction_validation"),
    ]

    for title, key in requirements:

        f.write("\n" + "=" * 90 + "\n")
        f.write(title + "\n")
        f.write("=" * 90 + "\n\n")

        item = evidence["client_requirements"][key]

        f.write("CLIENT REQUIREMENT:\n")
        f.write(item["requirement"] + "\n\n")

        results = item["evidence"]

        if not results:
            f.write("NO DIRECT IMPLEMENTATION EVIDENCE FOUND.\n")
            continue

        # Avoid overwhelming the final evidence file with duplicates.
        seen = set()

        for result in results:

            signature = (
                result["file"],
                result["matched"],
            )

            if signature in seen:
                continue

            seen.add(signature)

            f.write(f"FILE: {result['file']}\n")
            f.write(f"MATCH: {result['matched']}\n")
            f.write("-" * 70 + "\n")
            f.write(result["context"])
            f.write("\n\n")


# ================================================================
# JSON evidence
# ================================================================

with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        evidence,
        f,
        indent=2,
        ensure_ascii=False
    )


# ================================================================
# Console summary
# ================================================================

print("\n" + "=" * 90)
print("CLIENT FEEDBACK COVERAGE")
print("=" * 90)

requirements = [
    ("1. LLM USED", "1_llm_used"),
    ("2. PROMPT", "2_prompt"),
    ("3. JSON / SCHEMA", "3_json_schema"),
    ("4. MODEL SETTINGS", "4_model_settings"),
    ("5. COST / RATE-LIMIT", "5_cost_rate_limit"),
    ("6. CACHING", "6_caching"),
    ("7. FALLBACK / RETRY", "7_fallback_behavior"),
    ("8. VALIDATION", "8_extraction_validation"),
]

for label, key in requirements:

    count = len(
        evidence["client_requirements"][key]["evidence"]
    )

    status = "FOUND" if count else "NOT FOUND"

    print(f"{label:<35} : {status} ({count} matches)")


print("\n" + "=" * 90)
print("EVIDENCE FILES GENERATED")
print("=" * 90)

print(f"\nTXT:")
print(TXT_OUTPUT)

print(f"\nJSON:")
print(JSON_OUTPUT)

print("\nCompleted.")