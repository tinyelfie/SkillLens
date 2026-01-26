import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# -----------------------------
# IMPORTS
# -----------------------------
from rewriting.resume_optimiser.decision_engine import decide_rewrite_actions
from rewriting.resume_optimiser.rewriter import rewrite_resume
from retrieval.rag_pipeline.retriever import retrieve_relevant_chunks

# -----------------------------
# LOAD STEP 6 OUTPUT (FIXED)
# -----------------------------
SCORE_PATH = (
    PROJECT_ROOT
    / "matching"
    / "ranking_scoring"
    / "last_score.json"
)

with open(SCORE_PATH, "r", encoding="utf-8") as f:
    match_scores = json.load(f)

# -----------------------------
# DECIDE REWRITE ACTIONS
# -----------------------------
actions = decide_rewrite_actions(match_scores)
print("\nRewrite actions decided:", actions)

# -----------------------------
# RETRIEVE EVIDENCE (RAG)
# -----------------------------
resume_context = retrieve_relevant_chunks(
    query_text="relevant experience",
    namespace="resume",
    top_k=5
)

jd_context = retrieve_relevant_chunks(
    query_text="key responsibilities",
    namespace="jd",
    top_k=5
)

resume_text = "\n".join(resume_context)
jd_text = "\n".join(jd_context)

# -----------------------------
# REWRITE RESUME
# -----------------------------
optimized_resume = rewrite_resume(
    resume_context=resume_text,
    jd_context=jd_text
)

print("\n=== OPTIMIZED RESUME ===\n")
print(optimized_resume)

# -----------------------------
# SAVE OUTPUT FOR STEP 8
# -----------------------------
OUTPUT_PATH = (
    PROJECT_ROOT
    / "rewriting"
    / "resume_optimiser"
    / "output_resume.txt"
)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(optimized_resume)

