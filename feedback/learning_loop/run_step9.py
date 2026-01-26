import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from feedback_collector import collect_feedback
from feedback_store import save_feedback
from weight_updater import load_weights, update_weights

# -----------------------------
# LOAD LAST SCORE
# -----------------------------
SCORE_PATH = (
    PROJECT_ROOT
    / "matching"
    / "ranking_scoring"
    / "last_score.json"
)

with open(SCORE_PATH, "r", encoding="utf-8") as f:
    last_score = json.load(f)

# -----------------------------
# COLLECT FEEDBACK
# -----------------------------
feedback = collect_feedback()

# -----------------------------
# SAVE FEEDBACK
# -----------------------------
save_feedback({
    "score": last_score,
    **feedback
})

# -----------------------------
# UPDATE MODEL WEIGHTS
# -----------------------------
weights = load_weights()
updated_weights = update_weights(weights, feedback)

print("\n=== STEP 9 COMPLETE ===")
print("Feedback received:", feedback)
print("Updated scoring weights:", updated_weights)
