def calculate_risk(report):

    count = report.get("occurrence_count", 1)
    platform_count = len(report.get("sources_seen", []))

    risk_score = count * platform_count

    if risk_score >= 8:
        level = "HIGH"
    elif risk_score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": level
    }
