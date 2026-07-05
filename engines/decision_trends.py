def analyze_decision_trends(history):
    if not history:
        return {
            "count": 0,
            "average_gain": 0,
            "best_strategy": "Unknown",
            "most_common_intervention": "Unknown",
            "uncertainty_counts": {},
        }

    gains = [
        item.get("Projected Gain", 0)
        for item in history
    ]

    interventions = [
        item.get("Primary Intervention", "Unknown")
        for item in history
    ]

    uncertainty_counts = {}

    for item in history:
        uncertainty = item.get("Uncertainty", "Unknown")
        uncertainty_counts[uncertainty] = (
            uncertainty_counts.get(uncertainty, 0) + 1
        )

    intervention_counts = {}

    for intervention in interventions:
        intervention_counts[intervention] = (
            intervention_counts.get(intervention, 0) + 1
        )

    best = max(
        history,
        key=lambda item: item.get("Projected Gain", 0),
    )

    most_common_intervention = max(
        intervention_counts,
        key=intervention_counts.get,
    )

    return {
        "count": len(history),
        "average_gain": round(sum(gains) / len(gains), 2),
        "best_strategy": best.get("Recommended Strategy", "Unknown"),
        "best_gain": best.get("Projected Gain", 0),
        "most_common_intervention": most_common_intervention,
        "uncertainty_counts": uncertainty_counts,
    }