"""
Narrative intelligence and statistical computation
"""
from core.narratives.temporal_engine import compute_temporal_patterns
from core.narratives.state_engine import compute_narrative_state
from core.narratives.decay_engine import compute_memory_strength
from core.config import CRITICAL_THREAT_SCORE, HIGH_THREAT_SCORE, MEDIUM_THREAT_SCORE


def compute_narrative_stats(memories):
    """
    Compute comprehensive statistics for a narrative.
    
    Args:
        memories (list): List of memory payloads from Qdrant
        
    Returns:
        dict: Complete narrative statistics including threat assessment
    """
    years = []
    sources = set()
    modalities = set()
    claims = set()

    for m in memories:
        if m.get("year") and str(m.get("year")).isdigit():
            years.append(int(m["year"]))
        if m.get("source"):
            sources.add(m["source"])
        if m.get("type"):
            modalities.add(m["type"])
        if m.get("claim"):
            claims.add(m["claim"][:60])

    first_seen = min(years) if years else None
    last_seen = max(years) if years else None
    lifespan = last_seen - first_seen if first_seen and last_seen else 0

    resurfacing = lifespan >= 1 and len(memories) >= 3
    mutation_score = len(claims)

    base_stats = {
        "first_seen": first_seen,
        "last_seen": last_seen,
        "lifespan": lifespan,
        "sources": list(sources),
        "modalities": list(modalities),
        "mutation_score": mutation_score,
        "resurfacing": resurfacing
    }

    # Compute temporal patterns
    temporal = compute_temporal_patterns(memories)
    
    # Compute memory strength
    memory_strength = compute_memory_strength(memories, base_stats)
    
    # Compute narrative state
    state = compute_narrative_state(memories, base_stats)
    
    # 🆕 COMPUTE THREAT LEVEL
    threat_score = 0
    
    # Resurfacing increases threat
    if resurfacing:
        threat_score += 30
    
    # Multiple sources indicate spread
    if len(sources) >= 4:
        threat_score += 30
    elif len(sources) >= 3:
        threat_score += 20
    elif len(sources) >= 2:
        threat_score += 10
    
    # High mutation indicates evolution
    if mutation_score >= 5:
        threat_score += 25
    elif mutation_score >= 3:
        threat_score += 15
    
    # Long lifespan shows persistence
    if lifespan >= 3:
        threat_score += 25
    elif lifespan >= 2:
        threat_score += 15
    elif lifespan >= 1:
        threat_score += 10
    
    # Determine threat level
    if threat_score >= CRITICAL_THREAT_SCORE:
        threat_level = "CRITICAL"
    elif threat_score >= HIGH_THREAT_SCORE:
        threat_level = "HIGH"
    elif threat_score >= MEDIUM_THREAT_SCORE:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"
    
    # 🆕 COMPUTE NARRATIVE STRENGTH (0-100)
    strength = min(100, (
        len(memories) * 10 +           # Frequency
        len(sources) * 15 +             # Platform diversity
        lifespan * 10 +                 # Persistence
        (30 if resurfacing else 0)      # Resurfacing bonus
    ))

    return {
        **base_stats,
        "temporal_patterns": temporal,
        "memory_strength": memory_strength,
        "state": state,
        "threat_level": threat_level,      # ✅ Added
        "threat_score": threat_score,      # ✅ Added
        "strength": strength               # ✅ Added
    }