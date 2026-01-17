import uuid
from qdrant_client.http.models import PointStruct
from core.qdrant.client import client
from core.embeddings.image_embedder import embed_image


def store_image(image_path, metadata):

    vector = embed_image(image_path)

    client.upsert(
        collection_name="image_memory",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "type": "image",
                    "path": image_path,
                    **metadata
                }
            )
        ]
    )

    print("✅ Image stored in memory")
