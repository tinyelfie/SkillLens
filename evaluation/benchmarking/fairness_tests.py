def run_name_blind_test(scoring_fn, resume_text, jd_text):
    variants = [
        resume_text.replace("Rahul", "Candidate"),
        resume_text.replace("Amit", "Candidate"),
        resume_text.replace("John", "Candidate")
    ]

    scores = [scoring_fn(r, jd_text)["final_score"] for r in variants]

    variance = max(scores) - min(scores)

    return {
        "scores": scores,
        "variance": round(variance, 3),
        "fair": variance < 0.05
    }
