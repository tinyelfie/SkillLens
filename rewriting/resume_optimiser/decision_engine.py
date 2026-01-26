def decide_rewrite_actions(match_scores):
    actions = []

    if match_scores["skill_similarity"] < 0.75:
        actions.append("enhance_skills_section")

    if match_scores["experience_alignment"] < 0.7:
        actions.append("rewrite_experience_bullets")

    if match_scores["skill_coverage"] < 0.8:
        actions.append("emphasize_missing_skills")

    return actions
