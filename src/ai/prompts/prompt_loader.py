from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PROMPT_FILE = (
    ROOT
    / "src"
    / "ai"
    / "prompts"
    / "skill_extraction_v1.txt"
)

def load_prompt():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    print(load_prompt())