import sys
from pathlib import Path

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


import json
from feature_builder import (
    build_skill_match_features,
    build_experience_alignment
)
from scorer import compute_final_score


# -----------------------------
# LOAD DATA
# -----------------------------
from pathlib import Path
import json

# -----------------------------
# PROJECT ROOT
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESUME_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "resume_structured.json"
JD_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "jd_structured.json"

with open(RESUME_PATH, "r", encoding="utf-8") as f:
    resume = json.load(f)

with open(JD_PATH, "r", encoding="utf-8") as f:
    jd = json.load(f)


# Resume & JD components
resume_skills = resume.get("skills", [])
jd_skills = jd.get("required_skills", [])

resume_experience = [
    exp.get("description", "")
    for exp in resume.get("experience", [])
    if isinstance(exp, dict)
]

jd_responsibilities = jd.get("responsibilities", [])


# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
skill_sim, coverage = build_skill_match_features(
    resume_skills,
    jd_skills
)

experience_sim = build_experience_alignment(
    resume_experience,
    jd_responsibilities
)

# -----------------------------
# FINAL SCORING
# -----------------------------
result = compute_final_score(
    skill_sim,
    coverage,
    experience_sim
)

print("\n=== ATS MATCH SCORE ===")
for k, v in result.items():
    print(f"{k}: {v}")

import json
from pathlib import Path

# -----------------------------
# SAVE SCORE FOR STEP 7
# -----------------------------
OUTPUT_PATH = Path(__file__).resolve().parent / "last_score.json"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)


OUTPUT_PATH = Path(__file__).resolve().parent / "inferred_skills.json"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(
        {
            "ontology": inferred_skills,
            "soft": soft_inferred_skills
        },
        f,
        indent=2
    )
