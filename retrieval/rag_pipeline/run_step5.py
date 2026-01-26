import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from index_documents import index_chunks
from retriever import retrieve_relevant_chunks

# -----------------------------
# LOAD STRUCTURED DATA (SAFE)
# -----------------------------
RESUME_PATH = (
    PROJECT_ROOT
    / "embeddings"
    / "domain_embeddings"
    / "resume_structured.json"
)

JD_PATH = (
    PROJECT_ROOT
    / "embeddings"
    / "domain_embeddings"
    / "jd_structured.json"
)

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
# INDEX RESUME EXPERIENCE
# -----------------------------
resume_chunks = []

for exp in resume.get("experience", []):
    if isinstance(exp, dict):
        if "description" in exp:
            resume_chunks.append(exp["description"])
        elif "responsibilities" in exp:
            resume_chunks.append(exp["responsibilities"])
        else:
            resume_chunks.append(" ".join(str(v) for v in exp.values()))
    elif isinstance(exp, str):
        resume_chunks.append(exp)

index_chunks(
    chunks=resume_chunks,
    namespace="resume",
    metadata_type="resume_experience"
)

# -----------------------------
# INDEX JD RESPONSIBILITIES
# -----------------------------
jd_chunks = jd.get("responsibilities", [])

index_chunks(
    chunks=jd_chunks,
    namespace="jd",
    metadata_type="jd_responsibility"
)

# -----------------------------
# QUERY USING INFERRED SKILL
# -----------------------------
query = "Deep Learning experience"

retrieved_resume = retrieve_relevant_chunks(query, "resume")
retrieved_jd = retrieve_relevant_chunks(query, "jd")

print("\n=== RETRIEVED RESUME EVIDENCE ===")
for r in retrieved_resume:
    print("-", r)

print("\n=== RETRIEVED JD EVIDENCE ===")
for r in retrieved_jd:
    print("-", r)
