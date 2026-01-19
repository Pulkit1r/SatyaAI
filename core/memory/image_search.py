from core.qdrant.client import client
from core.embeddings.image_embedder import embed_image


def search_images(image_path, limit=5):
    """
    Search for similar images in memory.
    
    Args:
        image_path (str): Path to the image file
        limit (int): Maximum number of results
        
    Returns:
        list: List of search results with score and payload
    """
    vector = embed_image(image_path)

    try:
        # Try newer API first (query_points)
        results = client.query_points(
            collection_name="image_memory",
            query=vector,
            limit=limit
        )
        return results.points
    except AttributeError:
        # Fall back to older API (search)
        results = client.search(
            collection_name="image_memory",
            query_vector=vector,
            limit=limit
        )
        return results