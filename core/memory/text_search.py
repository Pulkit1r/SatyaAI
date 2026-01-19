from core.qdrant.client import client
from core.embeddings.text_embedder import embed_text


def search_claims(query, limit=5):
    """
    Search for similar claims in memory.
    
    Args:
        query (str): Search query text
        limit (int): Maximum number of results
        
    Returns:
        list: List of search results with score and payload
    """
    vector = embed_text(query)

    try:
        # Try newer API first (query_points)
        results = client.query_points(
            collection_name="text_memory",
            query=vector,
            limit=limit
        )
        return results.points
    except AttributeError:
        # Fall back to older API (search)
        results = client.search(
            collection_name="text_memory",
            query_vector=vector,
            limit=limit
        )
        return results