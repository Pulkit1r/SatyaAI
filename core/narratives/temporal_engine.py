def compute_temporal_patterns(memories):

    years = sorted([
        int(m.get("year")) for m in memories
        if m.get("year") and str(m.get("year")).isdigit()
    ])

    if len(years) < 2:
        return {
            "activity_years": years,
            "resurfacing_gaps": [],
            "seasonal": False
        }

    gaps = [years[i+1] - years[i] for i in range(len(years)-1)]
    seasonal = any(g >= 1 for g in gaps)

    return {
        "activity_years": years,
        "resurfacing_gaps": gaps,
        "seasonal": seasonal
    }
