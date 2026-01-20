from collections import defaultdict
from datetime import datetime


def build_timeline(results):
    """
    results: list of Qdrant search results
    Returns: {date: [platforms]}
    """

    timeline = defaultdict(list)

    for r in results:
        payload = r.payload

        ts = payload.get("timestamp")
        platform = payload.get("platform", "unknown")

        if ts:
            date_key = datetime.fromtimestamp(ts).date().isoformat()
            timeline[date_key].append(platform)

    return dict(timeline)
