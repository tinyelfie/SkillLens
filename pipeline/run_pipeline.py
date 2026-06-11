import json as _json

from parsing.resume_jd_structuring.extractor import (
    extract_resume_structure,
    extract_jd_structure
)
from matching.ranking_scoring.feature_builder import (
    build_skill_match_features,
    build_experience_alignment,
)
from matching.ranking_scoring.scorer import compute_final_score
from ontology.skill_gap_adapter import find_missing_skills
from rewriting.resume_optimiser.rewriter import rewrite_resume


def run_pipeline(resume_text: str, jd_text: str) -> dict:
    """
    Pure pipeline function.
    NO file I/O.
    NO FastAPI code.
    """

    # Step 2 — Structure raw text into JSON via LLM
    resume_structured = extract_resume_structure(resume_text)
    jd_structured = extract_jd_structure(jd_text)

    # Step 3 — Extract skill / experience lists
    resume_skills = resume_structured.get("skills", [])
    jd_skills = jd_structured.get("required_skills", [])

    resume_experience = [
        exp.get("description", "")
        for exp in resume_structured.get("experience", [])
        if isinstance(exp, dict)
    ]
    jd_responsibilities = jd_structured.get("responsibilities", [])

    # Step 6 — Build features and compute weighted ATS score
    skill_sim, coverage = build_skill_match_features(resume_skills, jd_skills)
    experience_sim = build_experience_alignment(resume_experience, jd_responsibilities)
    match_score = compute_final_score(skill_sim, coverage, experience_sim)

    # Step 4 — Find skill gaps using ontology inference
    missing_skills = find_missing_skills(resume_structured, jd_structured)

    # Step 7 — Rewrite résumé (pass readable JSON strings, not raw dicts)
    resume_context = _json.dumps(resume_structured, indent=2)
    jd_context = _json.dumps(jd_structured, indent=2)
    optimized_resume = rewrite_resume(resume_context, jd_context)

    return {
        "score": match_score,
        "missing_skills": missing_skills,
        "optimized_resume": optimized_resume,
    }
