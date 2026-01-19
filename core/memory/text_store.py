import uuid
from qdrant_client.http.models import PointStruct
from core.qdrant.client import client, TEXT_COLLECTION
from core.embeddings.text_embedder import embed_text


def store_claim(text, metadata: dict):
    vector = embed_text(text)

    client.upsert(
        collection_name=TEXT_COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "type": "text",
                    "claim": text,
                    **metadata
                }
            )
        ]
    )

    print("✅ Claim stored in text memory")
