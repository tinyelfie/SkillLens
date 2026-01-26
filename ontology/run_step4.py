import json
from pathlib import Path

from skill_graph import SkillGraph
from skill_inference import SkillInferenceEngine
import json
from pathlib import Path
from skill_graph import SkillGraph
from skill_inference import SkillInferenceEngine


# -----------------------------
# PROJECT ROOT
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Correct paths
RESUME_PATH = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "resume_structured.json"
ONTOLOGY_PATH = PROJECT_ROOT / "data" / "skill_ontology" / "skills.json"


# -----------------------------
# LOAD RESUME STRUCTURE
# -----------------------------
with open(RESUME_PATH, "r", encoding="utf-8") as f:
    resume = json.load(f)

observed_skills = resume.get("skills", [])


# -----------------------------
# SKILL INFERENCE
# -----------------------------
graph = SkillGraph(ONTOLOGY_PATH)
engine = SkillInferenceEngine(graph)

inferred_skills = engine.infer_parent_skills(observed_skills)


# -----------------------------
# OUTPUT
# -----------------------------
print("\n=== OBSERVED SKILLS ===")
print(observed_skills)

print("\n=== INFERRED SKILLS (WITH CONFIDENCE) ===")
for skill, conf in inferred_skills.items():
    print(f"{skill}: {round(conf, 2)}")

# -----------------------------
# Resolve project root safely
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

resume_path = PROJECT_ROOT / "embeddings" / "domain_embeddings" / "resume_structured.json"
ontology_path = PROJECT_ROOT / "data" / "skill_ontology" / "skills.json"

# -----------------------------
# Load resume skills
# -----------------------------
with open(resume_path, "r", encoding="utf-8") as f:
    resume = json.load(f)

observed_skills = resume.get("skills", [])

# -----------------------------
# Run inference
# -----------------------------
graph = SkillGraph(ONTOLOGY_PATH, ALIASES_PATH)
ALIASES_PATH = PROJECT_ROOT / "data" / "skill_ontology" / "aliases.json"

engine = SkillInferenceEngine(graph)

inferred_skills = engine.infer_parent_skills(observed_skills)
soft_inferred_skills = engine.soft_infer_skills(observed_skills)

print("\n=== OBSERVED SKILLS ===")
print(observed_skills)

print("\n=== ONTOLOGY-INFERRED SKILLS ===")
for skill, conf in inferred_skills.items():
    print(f"{skill}: {round(conf, 2)}")

print("\n=== SOFT (EMBEDDING) INFERRED SKILLS ===")
for skill, conf in soft_inferred_skills.items():
    print(f"{skill}: {conf}")
