def intervention_priority(
    signal,
    evidence,
    decision,
    authority,
    time,
    willingness,
):

    surfaces = {
        "Signal Visibility": signal,
        "Evidence Integrity": evidence,
        "Decision Capacity": decision,
        "Authority To Act": authority,
        "Remaining Time": time,
        "Correction Willingness": willingness,
    }

    recommendations = []

    for surface, value in surfaces.items():

        if value <= 1:
            priority = "CRITICAL"

        elif value == 2:
            priority = "HIGH"

        elif value == 3:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        recommendations.append(
            {
                "surface": surface,
                "score": value,
                "priority": priority,
            }
        )

    order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    recommendations.sort(
        key=lambda x: order[x["priority"]]
    )

    return recommendations