def build_intelligence(narratives):

    stats = []

    for nid, items in narratives.items():
        years = [int(i["year"]) for i in items if str(i.get("year","")).isdigit()]
        stats.append({
            "id": nid,
            "count": len(items),
            "first": min(years) if years else None,
            "last": max(years) if years else None,
            "platforms": len(set(i.get("source") for i in items))
        })

    return sorted(stats, key=lambda x: x["count"], reverse=True)
