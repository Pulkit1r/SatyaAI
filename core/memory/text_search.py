from core.qdrant.client import client
from core.embeddings.text_embedder import embed_text


def search_claims(query, limit=5):

    vector = embed_text(query)

    results = client.query_points(
        collection_name="claims_memory",
        query=vector,
        limit=limit
    )

    return results.points
