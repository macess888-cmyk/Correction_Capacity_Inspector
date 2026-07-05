def build_memory_insights(memory_results):
    if not memory_results:
        return {
            "count": 0,
            "top_strategy": "Unknown",
            "top_intervention": "Unknown",
            "average_gain": 0,
            "dominant_uncertainty": "Unknown",
            "insight": "No memory results available.",
        }

    gains = [
        item.get("gain", 0)
        for item in memory_results
    ]

    strategies = {}
    interventions = {}
    uncertainties = {}

    for item in memory_results:
        strategy = item.get("strategy", "Unknown")
        intervention = item.get("intervention", "Unknown")
        uncertainty = item.get("uncertainty", "Unknown")

        strategies[strategy] = strategies.get(strategy, 0) + 1
        interventions[intervention] = interventions.get(intervention, 0) + 1
        uncertainties[uncertainty] = uncertainties.get(uncertainty, 0) + 1

    top_strategy = max(strategies, key=strategies.get)
    top_intervention = max(interventions, key=interventions.get)
    dominant_uncertainty = max(uncertainties, key=uncertainties.get)

    average_gain = round(
        sum(gains) / len(gains),
        2,
    )

    insight = (
        f"{top_intervention} appears most often in matching memory, "
        f"with average gain +{average_gain}."
    )

    return {
        "count": len(memory_results),
        "top_strategy": top_strategy,
        "top_intervention": top_intervention,
        "average_gain": average_gain,
        "dominant_uncertainty": dominant_uncertainty,
        "insight": insight,
    }