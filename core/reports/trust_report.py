from core.memory.text_search import search_claims


def generate_trust_report(query):

    results = search_claims(query, limit=10)

    if not results:
        return {
            "status": "no_history",
            "message": "No similar claims found in memory."
        }

    narrative_id = results[0].payload.get("narrative_id", "Unknown")

    timeline = []
    sources = set()
    years = []

    for r in results:
        data = r.payload
        years.append(int(data.get("year", 0)) if data.get("year") else 0)

        timeline.append({
            "year": data.get("year"),
            "source": data.get("source"),
            "claim": data.get("claim"),
            "score": round(r.score, 3)
        })

        if data.get("source"):
            sources.add(data.get("source"))

    timeline = sorted(timeline, key=lambda x: (x["year"] or 0))

    first_seen = min([y for y in years if y != 0], default="Unknown")
    last_seen = max(years) if years else "Unknown"

    report = {
        "status": "history_found",
        "narrative_id": narrative_id,
        "occurrence_count": len(timeline),
        "first_seen": first_seen,
        "last_seen": last_seen,
        "sources_seen": list(sources),
        "timeline": timeline,
        "insight": f"This narrative first appeared in {first_seen} and resurfaced {len(timeline)} times across platforms."
    }

    return report
