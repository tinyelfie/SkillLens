def compute_final_score(skill_sim, coverage, experience_sim):
    """
    Weighted ATS-style scoring
    """
    weights = {
        "skill_similarity": 0.4,
        "coverage": 0.3,
        "experience": 0.3
    }

    final_score = (
        weights["skill_similarity"] * skill_sim +
        weights["coverage"] * coverage +
        weights["experience"] * experience_sim
    )

    explanation = {
        "skill_similarity": round(skill_sim, 2),
        "skill_coverage": round(coverage, 2),
        "experience_alignment": round(experience_sim, 2),
        "final_score": round(final_score, 2)
    }

    return explanation
