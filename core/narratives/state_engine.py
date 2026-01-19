from datetime import datetime

def compute_narrative_state(memories, stats):

    if not stats["first_seen"]:
        return "NEW"

    now_year = datetime.now().year
    last_seen = stats["last_seen"]
    count = len(memories)

    dormant_gap = now_year - last_seen

    if count == 1:
        return "NEW"

    if dormant_gap >= 2 and stats["resurfacing"]:
        return "RESURFACED"

    if dormant_gap >= 2:
        return "DORMANT"

    if count >= 5:
        return "ACTIVE"

    return "ACTIVE"
