import sys
from pathlib import Path

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from embeddings.domain_embeddings.embedder import embed_text
from pinecone_client import index


def index_chunks(chunks, namespace, metadata_type):
    vectors = []

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        vectors.append(
            (
                f"{metadata_type}_{i}",
                embedding,
                {"type": metadata_type, "text": chunk}
            )
        )

    index.upsert(vectors=vectors, namespace=namespace)
