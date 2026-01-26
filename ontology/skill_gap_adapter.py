from pathlib import Path
from ontology.skill_graph import SkillGraph
from ontology.skill_inference import SkillInferenceEngine


def find_missing_skills(resume_structured, jd_structured):
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    ontology_path = PROJECT_ROOT / "data" / "skill_ontology" / "skills.json"
    aliases_path = PROJECT_ROOT / "data" / "skill_ontology" / "aliases.json"

    graph = SkillGraph(ontology_path, aliases_path)
    engine = SkillInferenceEngine(graph)

    observed = resume_structured.get("skills", [])
    required = jd_structured.get("skills", [])

    inferred = engine.infer_parent_skills(observed)
    inferred.update(engine.soft_infer_skills(observed))

    missing = [
        skill for skill in required
        if skill not in observed and skill not in inferred
    ]

    return missing
