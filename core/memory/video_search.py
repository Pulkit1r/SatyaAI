"""
Video memory search operations
"""
from core.qdrant.client import client
from core.embeddings.image_embedder import embed_image


def search_video_frames(frame_path, limit=5):
    """
    Search for similar video frames in memory.
    
    Args:
        frame_path (str): Path to the frame image
        limit (int): Maximum number of results
        
    Returns:
        list: List of matching points with scores
    """
    vector = embed_image(frame_path)

    try:
        # Try newer API first (query_points)
        results = client.query_points(
            collection_name="video_memory",
            query=vector,
            limit=limit
        )
        return results.points
    except AttributeError:
        # Fall back to older API (search)
        results = client.search(
            collection_name="video_memory",
            query_vector=vector,
            limit=limit
        )
        return results