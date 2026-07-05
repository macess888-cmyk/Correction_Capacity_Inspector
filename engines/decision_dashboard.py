def build_decision_dashboard(
    plan,
    monte_carlo_result,
    sensitivity_rows,
    active_scenarios,
):
    top_scenario = None

    if active_scenarios:
        top_scenario = active_scenarios[0]

    projected_gain = (
        plan.total_gain
        if plan
        else 0
    )

    monte_average = (
        monte_carlo_result.get("average_gain", 0)
        if monte_carlo_result
        else 0
    )

    confidence_low = (
        monte_carlo_result.get("confidence_low", 0)
        if monte_carlo_result
        else 0
    )

    confidence_high = (
        monte_carlo_result.get("confidence_high", 0)
        if monte_carlo_result
        else 0
    )

    strongest_sensitivity = (
        sensitivity_rows[0]
        if sensitivity_rows
        else None
    )

    if confidence_high - confidence_low <= 0.5:
        uncertainty = "Low"
    elif confidence_high - confidence_low <= 1.5:
        uncertainty = "Medium"
    else:
        uncertainty = "High"

    return {
        "recommended_strategy": (
            top_scenario.name
            if top_scenario
            else "Current Scenario"
        ),
        "projected_gain": round(projected_gain, 2),
        "monte_carlo_average": round(monte_average, 2),
        "uncertainty": uncertainty,
        "confidence_range": (
            round(confidence_low, 2),
            round(confidence_high, 2),
        ),
        "most_sensitive_dependency": (
            strongest_sensitivity["Dependency"]
            if strongest_sensitivity
            else "Unknown"
        ),
        "sensitivity_level": (
            strongest_sensitivity["Influence"]
            if strongest_sensitivity
            else "Unknown"
        ),
        "primary_intervention": (
            plan.steps[0].intervention
            if plan and plan.steps
            else "None"
        ),
    }