import json
from pathlib import Path
from datetime import datetime

FEEDBACK_FILE = Path(__file__).resolve().parent / "feedback_log.json"

def save_feedback(data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        **data
    }

    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(record)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
