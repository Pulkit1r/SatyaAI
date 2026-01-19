def assess_responsibility(narrative_items):

    evidence = len(narrative_items)

    if evidence >= 6:
        strength = "High"
    elif evidence >= 3:
        strength = "Medium"
    else:
        strength = "Low"

    privacy_note = "No personal data detected"
    human_review = "Recommended" if evidence >= 3 else "Required"

    return {
        "evidence_strength": strength,
        "human_review": human_review,
        "privacy_note": privacy_note
    }
