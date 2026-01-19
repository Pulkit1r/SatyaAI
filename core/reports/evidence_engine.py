def compute_evidence_strength(stats):

    score = 0

    score += len(stats.get("sources", [])) * 10
    score += len(stats.get("modalities", [])) * 15
    score += stats.get("lifespan", 0) * 5
    score += stats.get("mutation_score", 0) * 4

    if stats.get("resurfacing"):
        score += 15

    return min(100, score)
                