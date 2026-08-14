"""
=========================================================
Skill Gap Analysis Engine
=========================================================
"""

import json

from src.normalization.config import PROJECT_ROOT


class SkillGapEngine:

    def __init__(self):

        # ----------------------------------------------------
        # Load Role Skill Matrix
        # ----------------------------------------------------

        matrix_file = (
            PROJECT_ROOT
            / "taxonomy"
            / "role_skill_matrix.json"
        )

        with open(matrix_file, "r", encoding="utf-8") as f:
            self.matrix = json.load(f)

        # ----------------------------------------------------
        # Load Learning Paths
        # ----------------------------------------------------

        learning_file = (
            PROJECT_ROOT
            / "taxonomy"
            / "learning_paths.json"
        )

        with open(learning_file, "r", encoding="utf-8") as f:
            self.learning = json.load(f)

        print("=" * 60)
        print("SKILL GAP ENGINE")
        print("=" * 60)
        print(f"Roles Loaded      : {len(self.matrix)}")
        print(f"Learning Paths    : {len(self.learning)}")

    # ----------------------------------------------------
    # Skill Gap Analysis
    # ----------------------------------------------------

    def analyze(self, role, normalized_skills):

        role = str(role).strip()

        if role not in self.matrix:

            return {
                "matched": [],
                "missing": [],
                "score": 0,
                "recommendations": []
            }

        required = self.matrix[role]["required"]

        detected = set()

        for skill in normalized_skills:

            if isinstance(skill, dict):

                normalized = (
                    skill.get("normalized", "")
                    .strip()
                    .lower()
                )

                if normalized:
                    detected.add(normalized)

        matched = []
        missing = []

        for skill in required:

            if skill.lower() in detected:
                matched.append(skill)
            else:
                missing.append(skill)

        # ----------------------------------------------------
        # Readiness Score
        # ----------------------------------------------------

        score = 0.0

        if required:
            score = round(
                (len(matched) / len(required)) * 100,
                2
            )

        # ----------------------------------------------------
        # Learning Recommendations
        # ----------------------------------------------------

        recommendations = []

        for skill in missing:

            key = skill.lower()

            if key in self.learning:

                recommendations.append({

                    "skill": skill,

                    "course":
                        self.learning[key]["course"],

                    "certification":
                        self.learning[key]["certification"]

                })

            else:

                recommendations.append({

                    "skill": skill,

                    "course":
                        f"Learn {skill.title()}",

                    "certification":
                        "N/A"

                })

        return {

            "matched": matched,

            "missing": missing,

            "score": score,

            "recommendations": recommendations

        }


# --------------------------------------------------------
# Test
# --------------------------------------------------------

if __name__ == "__main__":

    engine = SkillGapEngine()

    sample = [

        {"normalized": "business analysis"},
        {"normalized": "sql"},
        {"normalized": "power bi"}

    ]

    result = engine.analyze(

        "Business Analyst",

        sample

    )

    print("\nRESULT")
    print("=" * 60)
    print(json.dumps(result, indent=4))