from parsing.resume_jd_structuring.extractor import (
    extract_resume_structure,
    extract_jd_structure
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

    # Step 2
    resume_structured = extract_resume_structure(resume_text)
    jd_structured = extract_jd_structure(jd_text)

    # Step 4–6
    match_score = compute_final_score(resume_structured, jd_structured)
    missing_skills = find_missing_skills(resume_structured, jd_structured)

    # Step 7
    optimized_resume = rewrite_resume(resume_structured, jd_structured)

    return {
        "score": match_score,
        "missing_skills": missing_skills,
        "optimized_resume": optimized_resume
    }
