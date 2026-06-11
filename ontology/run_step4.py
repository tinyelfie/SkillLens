import sys
import json
from pathlib import Path

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from skill_graph import SkillGraph
from skill_inference import SkillInferenceEngine

# -----------------------------
# PATHS
# -----------------------------
RESUME_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "resume_structured.json"
ONTOLOGY_PATH = PROJECT_ROOT / "data" / "skill_ontology" / "skills.json"
ALIASES_PATH = PROJECT_ROOT / "data" / "skill_ontology" / "aliases.json"

if not RESUME_PATH.exists():
    raise FileNotFoundError(f"resume_structured.json not found at:\n{RESUME_PATH}\nRun Step 2 first.")

# -----------------------------
# LOAD RESUME STRUCTURE
# -----------------------------
with open(RESUME_PATH, "r", encoding="utf-8") as f:
    resume = json.load(f)

observed_skills = resume.get("skills", [])

# -----------------------------
# BUILD SKILL GRAPH
# -----------------------------
graph = SkillGraph(ONTOLOGY_PATH, ALIASES_PATH)
engine = SkillInferenceEngine(graph)

# -----------------------------
# RUN INFERENCE
# -----------------------------
inferred_skills = engine.infer_parent_skills(observed_skills)
soft_inferred_skills = engine.soft_infer_skills(observed_skills)

# -----------------------------
# OUTPUT
# -----------------------------
print("\n=== OBSERVED SKILLS ===")
print(observed_skills)

print("\n=== ONTOLOGY-INFERRED SKILLS ===")
for skill, conf in inferred_skills.items():
    print(f"  {skill}: {round(conf, 2)}")

print("\n=== SOFT (EMBEDDING) INFERRED SKILLS ===")
for skill, conf in soft_inferred_skills.items():
    print(f"  {skill}: {conf}")

print("\n✅ Step 4 complete.")
