from core.memory.text_search import search_claims
from core.narratives.narrative_intelligence import compute_narrative_stats
from core.reports.evidence_engine import compute_evidence_strength


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
    memories = []

    for r in results:
        data = r.payload

        memory = {
            "year": data.get("year"),
            "source": data.get("source"),
            "claim": data.get("claim"),
            "type": data.get("type", "text"),
            "score": round(r.score, 3)
        }

        memories.append(memory)
        timeline.append(memory)

        if data.get("source"):
            sources.add(data.get("source"))

    timeline = sorted(
        timeline,
        key=lambda x: int(x["year"]) if x["year"] and str(x["year"]).isdigit() else 0
    )

    stats = compute_narrative_stats(memories)

    evidence = compute_evidence_strength(stats)

    report = {
        "status": "history_found",
        "narrative_id": narrative_id,
        "occurrence_count": len(memories),
        "sources_seen": list(sources),
        "timeline": timeline,
        "insight": f"This narrative first appeared in {stats['first_seen']} and has resurfaced {len(memories)} times over time."
    }

    report.update({
        "first_seen": stats["first_seen"],
        "last_seen": stats["last_seen"],
        "lifespan": stats["lifespan"],
        "modalities": stats["modalities"],
        "strength": stats["strength"],
        "threat_level": stats["threat_level"],
        "resurfacing": stats["resurfacing"],
        "narrative_state": stats["state"],
        "memory_strength": stats["memory_strength"],
        "temporal_patterns": stats["temporal_patterns"]
    })


    report.update({
        "evidence_strength": evidence
    })

    return report
