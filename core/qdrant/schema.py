from qdrant_client.http.models import Distance, VectorParams
from core.qdrant.client import client


def setup_collections():
    """Setup Qdrant collections with proper error handling"""
    
    collections = {
        "text_memory": 384,     # MiniLM
        "image_memory": 512,    # CLIP
        "video_memory": 512     # CLIP frames
    }

    for name, size in collections.items():
        try:
            # Try to get collection info
            client.get_collection(name)
            print(f"✓ Collection already exists: {name}")
        except Exception:
            # Collection doesn't exist, create it
            try:
                client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(
                        size=size,
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created collection: {name}")
            except Exception as e:
                print(f"❌ Error creating {name}: {e}")


if __name__ == "__main__":
    setup_collections()