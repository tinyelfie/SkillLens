# embeddings/domain_embeddings/embedder.py

from sentence_transformers import SentenceTransformer

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text: str) -> list:
    _load_model()
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
