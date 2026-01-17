from core.qdrant.client import client


def get_all_narratives():

    points = client.scroll(
        collection_name="claims_memory",
        limit=100
    )[0]

    narratives = {}

    for p in points:
        nid = p.payload.get("narrative_id", "unknown")
        if nid not in narratives:
            narratives[nid] = []
        narratives[nid].append(p.payload)

    return narratives
