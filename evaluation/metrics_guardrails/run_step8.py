import sys
from pathlib import Path
import json

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from factual_checker import detect_new_claims
from grounding_checker import check_grounding
from llm_judge import llm_judge
from retrieval.rag_pipeline.retriever import retrieve_relevant_chunks

# -----------------------------
# LOAD REWRITTEN RESUME (SAFE)
# -----------------------------
OUTPUT_RESUME_PATH = (
    PROJECT_ROOT
    / "rewriting"
    / "resume_optimiser"
    / "output_resume.txt"
)

if not OUTPUT_RESUME_PATH.exists():
    raise FileNotFoundError(
        f"output_resume.txt not found at:\n{OUTPUT_RESUME_PATH}\n"
        "Run Step 7 first."
    )

with open(OUTPUT_RESUME_PATH, "r", encoding="utf-8") as f:
    rewritten_resume = f.read()

# -----------------------------
# LOAD STRUCTURED INPUTS (SAFE)
# -----------------------------
RESUME_STRUCTURED_PATH = (
    PROJECT_ROOT
    / "embeddings"
    / "domain_embeddings"
    / "resume_structured.json"
)

JD_STRUCTURED_PATH = (
    PROJECT_ROOT
    / "embeddings"
    / "domain_embeddings"
    / "jd_structured.json"
)

if not RESUME_STRUCTURED_PATH.exists():
    raise FileNotFoundError(f"Missing file: {RESUME_STRUCTURED_PATH}")

if not JD_STRUCTURED_PATH.exists():
    raise FileNotFoundError(f"Missing file: {JD_STRUCTURED_PATH}")

with open(RESUME_STRUCTURED_PATH, "r", encoding="utf-8") as f:
    resume_structured = json.load(f)

with open(JD_STRUCTURED_PATH, "r", encoding="utf-8") as f:
    jd_structured = json.load(f)

original_text = " ".join(resume_structured.get("skills", []))

# -----------------------------
# RETRIEVE EVIDENCE
# -----------------------------
evidence = retrieve_relevant_chunks(
    query_text="experience",
    namespace="resume",
    top_k=5
)

# -----------------------------
# CHECKS
# -----------------------------
fact_ok, new_tokens = detect_new_claims(
    original_text,
    rewritten_resume
)

ground_ok, grounding_score = check_grounding(
    rewritten_resume,
    evidence
)

judge_result = llm_judge(
    original_text,
    rewritten_resume,
    " ".join(jd_structured.get("responsibilities", []))
)

# -----------------------------
# FINAL DECISION
# -----------------------------
print("\n=== STEP 8 EVALUATION ===")
print("Factual consistency:", fact_ok)
print("Grounded:", ground_ok, "| score:", round(grounding_score, 2))
print("LLM Judge:", judge_result)

if fact_ok and ground_ok:
    print("\n✅ Resume PASSED guardrails")
else:
    print("\n❌ Resume FAILED guardrails — do not show to user")
