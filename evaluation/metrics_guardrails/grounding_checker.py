from embeddings.domain_embeddings.embedder import embed_text
from matching.ranking_scoring.similarity import cosine_similarity


def check_grounding(rewritten_text, evidence_chunks, threshold=0.7):
    rewritten_emb = embed_text(rewritten_text)

    scores = []
    for chunk in evidence_chunks:
        chunk_emb = embed_text(chunk)
        scores.append(cosine_similarity(rewritten_emb, chunk_emb))

    max_score = max(scores) if scores else 0.0

    return max_score >= threshold, max_score
