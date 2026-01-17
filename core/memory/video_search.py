from core.qdrant.client import client
from core.embeddings.image_embedder import embed_image


VIDEO_COLLECTION = "video_memory"


def search_video_frames(frame_path, limit=5):
    vector = embed_image(frame_path)

    results = client.query_points(
        collection_name=VIDEO_COLLECTION,
        query=vector,
        limit=limit
    )

    return results
