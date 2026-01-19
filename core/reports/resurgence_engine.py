def calculate_resurgence(narrative_items):
    years = [int(i["year"]) for i in narrative_items if str(i.get("year","")).isdigit()]
    platforms = set(i.get("source") for i in narrative_items)

    frequency_score = min(len(narrative_items) * 10, 40)
    diversity_score = min(len(platforms) * 10, 30)

    gap_score = 0
    if len(years) >= 2:
        span = max(years) - min(years)
        if span >= 3: gap_score = 30
        elif span == 2: gap_score = 20
        elif span == 1: gap_score = 10

    total = frequency_score + diversity_score + gap_score

    if total > 70: label = "High"
    elif total > 40: label = "Medium"
    else: label = "Low"

    return {
        "resurgence_score": min(total, 100),
        "resurgence_risk": label
    }
