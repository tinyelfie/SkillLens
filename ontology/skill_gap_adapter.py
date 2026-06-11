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

    # JD schema uses "required_skills" and "preferred_skills", not "skills"
    required = (
        jd_structured.get("required_skills", []) +
        jd_structured.get("preferred_skills", [])
    )

    inferred = engine.infer_parent_skills(observed)
    inferred.update(engine.soft_infer_skills(observed))

    observed_set = set(s.lower() for s in observed)
    inferred_set = set(s.lower() for s in inferred)

    missing = [
        skill for skill in required
        if skill.lower() not in observed_set and skill.lower() not in inferred_set
    ]

    return missing
