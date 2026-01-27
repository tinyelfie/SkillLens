import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="resume_jd_embeddings"
)


def add_document(doc_id: str, text: str, embedding: list, metadata: dict):
    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[doc_id]
    )


def query_similar(embedding: list, top_k: int = 5):
    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
