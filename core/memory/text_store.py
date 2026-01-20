import time
import uuid
from qdrant_client.http.models import PointStruct
from core.qdrant.client import client, TEXT_COLLECTION
from core.embeddings.text_embedder import embed_text


def store_claim(text, metadata: dict):
    vector = embed_text(text)

    payload = {
        "type": "text",
        "claim": text,
        "timestamp": time.time(),              # ✅ REQUIRED
        "source": metadata.get("source"),      # twitter, whatsapp, etc.
        "platform": metadata.get("source"),    # kept separate for future use
        "year": metadata.get("year")
    }

    client.upsert(
        collection_name=TEXT_COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )
        ]
    )

    print("✅ Claim stored with timestamp + platform")
