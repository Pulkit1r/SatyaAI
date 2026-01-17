from core.qdrant.client import client
from core.embeddings.image_embedder import embed_image


def search_images(image_path, limit=5):

    vector = embed_image(image_path)

    results = client.query_points(
        collection_name="image_memory",
        query=vector,
        limit=limit
    )

    return results.points
