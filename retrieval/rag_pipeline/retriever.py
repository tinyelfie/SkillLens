import sys
from pathlib import Path

# -----------------------------
# ADD PROJECT ROOT TO PATH
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# -----------------------------
# CORRECT IMPORTS (ABSOLUTE)
# -----------------------------
from retrieval.rag_pipeline.pinecone_client import index
from embeddings.domain_embeddings.embedder import embed_text


def retrieve_relevant_chunks(query_text, namespace, top_k=5):
    query_embedding = embed_text(query_text)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    return [match["metadata"]["text"] for match in results["matches"]]
