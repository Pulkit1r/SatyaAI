import uuid
from datetime import datetime
from typing import List, Dict

from qdrant_client.http.models import PointStruct
from core.qdrant.client import client, TEXT_COLLECTION
from core.embeddings.text_embedder import embed_text


def store_claim(text: str, metadata: Dict):
    """
    Store a text claim in Qdrant with metadata.
    """
    vector = embed_text(text)

    payload = {
        "type": "text",
        "claim": text,
        "created_at": datetime.utcnow().isoformat(),
        **metadata
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

    print("✅ Claim stored in text memory")


def query_claims(query_text: str, top_k: int = 5) -> List[Dict]:
    """
    Query similar claims from Qdrant and return explainable results.
    """
    query_vector = embed_text(query_text)

    search_results = client.search(
        collection_name=TEXT_COLLECTION,
        query_vector=query_vector,
        limit=top_k
    )

    formatted_results = []

    for r in search_results:
        formatted_results.append({
            "claim": r.payload.get("claim", ""),
            "score": round(r.score, 3),
            "source": r.payload.get("source", "unknown"),
            "created_at": r.payload.get("created_at", "unknown")
        })

    return formatted_results
