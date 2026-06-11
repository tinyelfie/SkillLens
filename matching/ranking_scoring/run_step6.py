import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from feature_builder import (
    build_skill_match_features,
    build_experience_alignment
)
from scorer import compute_final_score


# -----------------------------
# LOAD DATA
# -----------------------------
RESUME_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "resume_structured.json"
JD_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "jd_structured.json"

if not RESUME_PATH.exists():
    raise FileNotFoundError(f"resume_structured.json not found at:\n{RESUME_PATH}\nRun Step 2 first.")

if not JD_PATH.exists():
    raise FileNotFoundError(f"jd_structured.json not found at:\n{JD_PATH}\nRun Step 2 first.")

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

# -----------------------------
# SAVE SCORE FOR STEP 7
# -----------------------------
OUTPUT_PATH = Path(__file__).resolve().parent / "last_score.json"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"\n✅ Saved score to: {OUTPUT_PATH}")
