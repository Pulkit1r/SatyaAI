from qdrant_client.http.models import Distance, VectorParams
from core.qdrant.client import client


def setup_collections():

    collections = {
        "text_memory": 384,     # MiniLM
        "image_memory": 512,    # CLIP
        "video_memory": 512     # CLIP frames
    }

    for name, size in collections.items():
        if not client.collection_exists(name):
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=size,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created collection: {name}")
        else:
            print(f"✔ Collection already exists: {name}")


if __name__ == "__main__":
    setup_collections()
