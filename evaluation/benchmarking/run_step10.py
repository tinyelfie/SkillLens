import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from quality_metrics import quality_report
from fairness_tests import run_name_blind_test
from robustness_tests import robustness_check

# -----------------------------
# LOAD SCORES (SAFE)
# -----------------------------
SCORE_PATH = (
    PROJECT_ROOT
    / "matching"
    / "ranking_scoring"
    / "last_score.json"
)

if not SCORE_PATH.exists():
    raise FileNotFoundError(
        f"last_score.json not found at:\n{SCORE_PATH}\n"
        "Run Step 6 first."
    )

with open(SCORE_PATH, "r", encoding="utf-8") as f:
    after_score = json.load(f)

# -----------------------------
# SIMULATED BASELINE (PRE-OPTIMIZATION)
# -----------------------------
before_score = {
    "skill_similarity": after_score["skill_similarity"] - 0.1,
    "experience_alignment": after_score["experience_alignment"] - 0.1,
    "final_score": after_score["final_score"] - 0.1
}

# -----------------------------
# QUALITY EVALUATION
# -----------------------------
quality = quality_report(before_score, after_score)

print("\n=== QUALITY METRICS ===")
print(quality)

# -----------------------------
# FAIRNESS & ROBUSTNESS TESTS
# -----------------------------
def dummy_scoring(resume, jd):
    return after_score

fairness = run_name_blind_test(
    dummy_scoring,
    "Rahul has experience in ML",
    "ML Engineer role"
)

robustness = robustness_check(
    dummy_scoring,
    "Developed ML pipelines",
    "ML Engineer role"
)

print("\n=== FAIRNESS TEST ===")
print(fairness)

print("\n=== ROBUSTNESS TEST ===")
print(robustness)
