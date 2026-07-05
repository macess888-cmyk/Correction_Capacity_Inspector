def build_adaptive_recommendation(
    learning,
    quality,
    trends,
):
    recommendation = "Continue collecting decision history."
    priority = "Low"
    reasons = []

    if learning.get("successful_intervention") != "Unknown":
        recommendation = (
            f"Prioritize {learning['successful_intervention']} "
            f"in future planning cycles."
        )
        priority = "Medium"

        reasons.append(
            f"{learning['successful_intervention']} appears repeatedly "
            f"in historical decisions."
        )

    if quality.get("quality_state") == "Strong":
        priority = "High"
        reasons.append(
            "Decision quality is currently strong."
        )

    elif quality.get("quality_state") in ["Weak", "Critical"]:
        recommendation = (
            "Review dependency assumptions before relying on recommendations."
        )
        priority = "High"

        reasons.append(
            "Decision quality is weak or critical."
        )

    if trends.get("average_gain", 0) <= 0:
        recommendation = (
            "Investigate why recent planning cycles are not producing gains."
        )
        priority = "High"

        reasons.append(
            "Average historical gain is non-positive."
        )

    if not reasons:
        reasons.append(
            "Insufficient historical signal for a stronger recommendation."
        )

    return {
        "recommendation": recommendation,
        "priority": priority,
        "reasons": reasons,
    }