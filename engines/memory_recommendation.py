def build_memory_recommendation(memory_insights):
    if not memory_insights or memory_insights["count"] == 0:
        return {
            "recommendation": "Continue accumulating decision memory.",
            "priority": "Low",
            "reason": "No matching decision memory exists yet.",
        }

    intervention = memory_insights["top_intervention"]
    average_gain = memory_insights["average_gain"]
    uncertainty = memory_insights["dominant_uncertainty"]

    if average_gain >= 5 and uncertainty != "High":
        return {
            "recommendation": f"Consider prioritizing {intervention}.",
            "priority": "High",
            "reason": (
                f"{intervention} appears frequently in memory "
                f"with average gain +{average_gain}."
            ),
        }

    if uncertainty == "High":
        return {
            "recommendation": (
                "Review assumptions before reusing this memory pattern."
            ),
            "priority": "Medium",
            "reason": "Matching memory is dominated by high uncertainty.",
        }

    return {
        "recommendation": f"Keep observing {intervention}.",
        "priority": "Medium",
        "reason": (
            f"{intervention} appears in memory, "
            f"but signal strength is not yet decisive."
        ),
    }