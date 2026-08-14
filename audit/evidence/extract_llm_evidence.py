import json

path = r"audit\evidence\outputs\06_llm_implementation\04B_3_LLM_IMPLEMENTATION_EVIDENCE.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

sections = data["client_requirements"]

keys = [
    "1_llm_used",
    "2_prompt",
    "3_json_schema",
    "4_model_settings",
    "5_cost_rate_limit",
    "6_caching",
    "7_fallback_behavior",
    "8_extraction_validation",
]

for key in keys:
    print("\n" + "=" * 90)
    print(key.upper())
    print("=" * 90)

    results = sections[key]["evidence"]

    if not results:
        print("NO EVIDENCE FOUND")
        continue

    # Show first 3 matches only
    for item in results[:3]:
        print("\nFILE:", item["file"])
        print("MATCH:", item["matched"])
        print("-" * 70)
        print(item["context"][:2000])