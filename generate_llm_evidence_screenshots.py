from pathlib import Path
import textwrap
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "audit" / "evidence" / "outputs" / "06_llm_implementation" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

def read(path):
    p = ROOT / path
    if not p.exists():
        return [f"[FILE NOT FOUND: {path}]"]
    return p.read_text(encoding="utf-8", errors="ignore").splitlines()

def block(lines, terms, limit=45):
    for i, line in enumerate(lines):
        if any(t.lower() in line.lower() for t in terms):
            return lines[i:min(len(lines), i + limit)]
    return ["[CODE SECTION NOT FOUND]"]

def card(name, title, source, lines):
    out = []
    for i, line in enumerate(lines, 1):
        parts = textwrap.wrap(line, 115, replace_whitespace=False) or [""]
        for j, part in enumerate(parts):
            out.append(f"{i:03d} | {part}" if j == 0 else f"    | {part}")
    fig = plt.figure(figsize=(16, max(6, min(18, 1.8 + .25*len(out)))))
    fig.text(.03, .965, title, fontsize=18, fontweight="bold", va="top")
    fig.text(.03, .925, f"Source: {source}", fontsize=10, va="top")
    fig.text(.03, .885, "\n".join(out), family="monospace", fontsize=9.5, va="top", linespacing=1.25)
    plt.axis("off")
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=.25)
    plt.close(fig)

settings = read("src/config/settings.py")
groq = read("src/ai/clients/groq_client.py")

card("01_model_configuration.png", "Figure 4B.3 — LLM Model Configuration",
     "src/config/settings.py", block(settings, ["MODEL_NAME", "TEMPERATURE", "MAX_TOKENS"], 20))

card("02_groq_client_configuration.png", "Figure 4B.4 — Groq Client and Structured JSON Configuration",
     "src/ai/clients/groq_client.py", block(groq, ["response = self.client.chat.completions.create"], 32))

card("06_retry_backoff.png", "Figure 4B.8 — Retry and Exponential Backoff Mechanism",
     "src/ai/clients/groq_client.py", block(groq, ["@retry("], 18))

card("07_json_validation.png", "Figure 4B.9 — JSON Response Parsing and Validation",
     "src/ai/clients/groq_client.py", block(groq, ["result = response.choices[0].message.content"], 12))

prompt_paths = [
    "src/ai/prompts/skill_extraction_prompt.txt",
    "src/ai/prompts/prompt.txt",
    "src/ai/prompts/system_prompt.txt",
]
prompt_path = next((p for p in prompt_paths if (ROOT/p).exists()), None)

if prompt_path:
    prompt = read(prompt_path)
    card("03_prompt_rules.png", "Figure 4B.5 — LLM Skill Extraction Prompt and Classification Rules",
         prompt_path, block(prompt, ["IMPORTANT RULES", "EDGE CASES", "TECHNOLOGY VS RESPONSIBILITY"], 45))
    card("04_prompt_exclusions.png", "Figure 4B.6 — Prompt Edge Cases and Exclusion Rules",
         prompt_path, block(prompt, ["DO NOT EXTRACT", "RULE 15", "REPEATED SKILLS"], 45))
    card("05_few_shot_schema.png", "Figure 4B.7 — Few-Shot Examples and JSON Output Schema",
         prompt_path, block(prompt, ["FEW SHOT EXAMPLES", "EXAMPLE 1", "OUTPUT"], 55))
else:
    for n, title in [
        ("03_prompt_rules.png", "Figure 4B.5 — LLM Skill Extraction Prompt and Classification Rules"),
        ("04_prompt_exclusions.png", "Figure 4B.6 — Prompt Edge Cases and Exclusion Rules"),
        ("05_few_shot_schema.png", "Figure 4B.7 — Few-Shot Examples and JSON Output Schema")]:
        card(n, title, "Prompt file path not found", ["Update the prompt path in this script and regenerate."])

integration_paths = ["app/app.py", "src/app.py", "src/pipeline.py"]
integration = next((p for p in integration_paths if (ROOT/p).exists()), None)
card("08_extraction_integration.png", "Figure 4B.10 — LLM Extraction Integration with the Application Pipeline",
     integration or "Application file not found", block(read(integration) if integration else [], ["GroqClient", "extract(", "normalize", "predict"], 50) if integration else ["Update integration path in this script and regenerate."])

(OUT/"README.txt").write_text(
"""4B.3 SCREENSHOT EVIDENCE
01_model_configuration.png - model/settings
02_groq_client_configuration.png - Groq/JSON configuration
03_prompt_rules.png - extraction rules
04_prompt_exclusions.png - edge cases/exclusions
05_few_shot_schema.png - examples/schema
06_retry_backoff.png - retry/backoff
07_json_validation.png - JSON parsing
08_extraction_integration.png - application integration
""", encoding="utf-8")

print("Generated screenshot evidence in:")
print(OUT)
for p in sorted(OUT.glob("*.png")):
    print(p.name)