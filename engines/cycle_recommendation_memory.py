def build_cycle_recommendation_memory(
    cycle_learning,
    cycle_trends,
):
    maturity = cycle_learning.get(
        "cycle_maturity",
        "Unknown",
    )

    trend = cycle_trends.get(
        "trend",
        "Unknown",
    )

    dominant_priority = cycle_trends.get(
        "dominant_priority",
        "Unknown",
    )

    if maturity == "Mature" and trend in ["Stable", "Improving"]:
        recommendation = (
            "Continue using the current decision cycle structure."
        )
        priority = "Low"

    elif maturity == "Developing":
        recommendation = (
            "Strengthen incomplete cycle stages before expanding complexity."
        )
        priority = "Medium"

    else:
        recommendation = (
            "Review cycle structure before relying on recommendations."
        )
        priority = "High"

    return {
        "cycle_maturity": maturity,
        "cycle_trend": trend,
        "dominant_priority": dominant_priority,
        "recommendation": recommendation,
        "priority": priority,
    }