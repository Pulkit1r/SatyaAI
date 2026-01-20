def calculate_trust_score(similarity: float, occurrences: int, source_count: int) -> dict:
    """
    similarity: 0–1 (higher = more similar to known misinformation)
    occurrences: how many times claim reappeared
    source_count: number of unique platforms/sources
    """

    risk = (
        similarity * 0.5 +
        min(occurrences / 10, 1.0) * 0.3 +
        min(source_count / 5, 1.0) * 0.2
    )

    trust_score = int((1 - risk) * 100)

    label = "High Risk" if trust_score < 40 else "Medium Risk" if trust_score < 70 else "Low Risk"

    return {
        "trust_score": trust_score,
        "risk_level": label
    }
