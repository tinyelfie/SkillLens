def score_improvement(before_score, after_score):
    return round(after_score - before_score, 3)


def quality_report(before, after):
    return {
        "skill_gain": score_improvement(
            before["skill_similarity"], after["skill_similarity"]
        ),
        "experience_gain": score_improvement(
            before["experience_alignment"], after["experience_alignment"]
        ),
        "final_score_gain": score_improvement(
            before["final_score"], after["final_score"]
        )
    }
