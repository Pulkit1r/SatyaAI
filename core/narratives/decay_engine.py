from datetime import datetime

def compute_memory_strength(memories, stats):

    base = len(memories)
    lifespan = stats.get("lifespan", 0)
    resurfacing = stats.get("resurfacing", False)

    strength = base + lifespan

    if resurfacing:
        strength += 5

    now_year = datetime.now().year
    last_seen = stats.get("last_seen")

    if last_seen and now_year - last_seen >= 3:
        strength -= 3  # decay

    return max(1, strength)
