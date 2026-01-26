import json
from pathlib import Path

WEIGHT_FILE = Path(__file__).resolve().parent / "scoring_weights.json"

DEFAULT_WEIGHTS = {
    "skill_similarity": 0.4,
    "coverage": 0.3,
    "experience": 0.3
}

def load_weights():
    if WEIGHT_FILE.exists():
        with open(WEIGHT_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_WEIGHTS.copy()

def update_weights(weights, feedback):
    lr = 0.05  # learning rate

    if feedback["accepted"]:
        weights["skill_similarity"] += lr
        weights["experience"] += lr
    else:
        weights["skill_similarity"] -= lr
        weights["coverage"] += lr

    # Normalize
    total = sum(weights.values())
    for k in weights:
        weights[k] /= total

    with open(WEIGHT_FILE, "w") as f:
        json.dump(weights, f, indent=2)

    return weights
