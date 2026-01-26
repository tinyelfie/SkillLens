from embeddings.domain_embeddings.embedder import embed_text
from similarity import cosine_similarity


def build_skill_match_features(resume_skills, jd_skills):
    """
    Returns:
    - average skill similarity
    - skill coverage ratio
    """
    similarities = []

    for jd_skill in jd_skills:
        jd_emb = embed_text(jd_skill)

        max_sim = 0.0
        for res_skill in resume_skills:
            res_emb = embed_text(res_skill)
            sim = cosine_similarity(jd_emb, res_emb)
            max_sim = max(max_sim, sim)

        similarities.append(max_sim)

    avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
    coverage = sum(1 for s in similarities if s > 0.7) / len(similarities) if similarities else 0.0

    return avg_similarity, coverage


def build_experience_alignment(resume_chunks, jd_chunks):
    """
    Measures how well resume experience aligns with JD responsibilities
    """
    scores = []

    for jd in jd_chunks:
        jd_emb = embed_text(jd)

        max_sim = 0.0
        for res in resume_chunks:
            res_emb = embed_text(res)
            sim = cosine_similarity(jd_emb, res_emb)
            max_sim = max(max_sim, sim)

        scores.append(max_sim)

    return sum(scores) / len(scores) if scores else 0.0
