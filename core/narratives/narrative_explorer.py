from collections import defaultdict
from core.qdrant.client import client, TEXT_COLLECTION, IMAGE_COLLECTION, VIDEO_COLLECTION

def get_all_narratives(limit=1000):
    narratives = defaultdict(list)

    for collection in [TEXT_COLLECTION, IMAGE_COLLECTION, VIDEO_COLLECTION]:
        try:
            points, _ = client.scroll(collection_name=collection, limit=limit)
        except:
            continue

        for p in points:
            payload = p.payload or {}
            nid = payload.get("narrative_id")

            if nid:
                narratives[nid].append(payload)

    return narratives
