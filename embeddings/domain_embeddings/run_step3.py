import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from embedder import embed_text
from vector_store import add_document

# -----------------------------
# LOAD STRUCTURED OUTPUTS (SAFE)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

RESUME_PATH = BASE_DIR / "resume_structured.json"
JD_PATH = BASE_DIR / "jd_structured.json"

if not RESUME_PATH.exists():
    raise FileNotFoundError(
        f"resume_structured.json not found at:\n{RESUME_PATH}\n"
        "Run Step 2 first."
    )

if not JD_PATH.exists():
    raise FileNotFoundError(
        f"jd_structured.json not found at:\n{JD_PATH}\n"
        "Run Step 2 first."
    )

with open(RESUME_PATH, "r", encoding="utf-8") as f:
    resume = json.load(f)

with open(JD_PATH, "r", encoding="utf-8") as f:
    jd = json.load(f)

# -----------------------------
# EMBED RESUME SKILLS
# -----------------------------
for i, skill in enumerate(resume.get("skills", [])):
    emb = embed_text(skill)
    add_document(
        doc_id=f"resume_skill_{i}",
        text=skill,
        embedding=emb,
        metadata={"type": "resume_skill"}
    )

# -----------------------------
# EMBED JD REQUIRED SKILLS
# -----------------------------
for i, skill in enumerate(jd.get("required_skills", [])):
    emb = embed_text(skill)
    add_document(
        doc_id=f"jd_skill_{i}",
        text=skill,
        embedding=emb,
        metadata={"type": "jd_required_skill"}
    )

print("✅ Step 3 embeddings stored successfully.")
