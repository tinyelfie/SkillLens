def robustness_check(scoring_fn, resume_text, jd_text):
    perturbed = resume_text.replace("developed", "worked on")

    base_score = scoring_fn(resume_text, jd_text)["final_score"]
    perturbed_score = scoring_fn(perturbed, jd_text)["final_score"]

    delta = abs(base_score - perturbed_score)

    return {
        "base_score": base_score,
        "perturbed_score": perturbed_score,
        "delta": round(delta, 3),
        "stable": delta < 0.05
    }
