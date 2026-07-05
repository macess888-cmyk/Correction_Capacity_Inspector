def build_recommendation_rationale(
    dashboard,
    plan,
    monte_carlo_result,
    sensitivity_rows,
):
    reasons = []

    if dashboard["projected_gain"] > 0:
        reasons.append(
            f"Projected planner gain is +{dashboard['projected_gain']:.2f}."
        )

    if dashboard["monte_carlo_average"] > 0:
        reasons.append(
            f"Monte Carlo average gain is +{dashboard['monte_carlo_average']:.2f}."
        )

    if dashboard["uncertainty"] == "Low":
        reasons.append(
            "Uncertainty is low across the confidence range."
        )
    elif dashboard["uncertainty"] == "Medium":
        reasons.append(
            "Uncertainty is moderate and should be monitored."
        )
    else:
        reasons.append(
            "Uncertainty is high; recommendation should be treated cautiously."
        )

    if dashboard["primary_intervention"] != "None":
        reasons.append(
            f"Primary intervention surface is {dashboard['primary_intervention']}."
        )

    if sensitivity_rows:
        top = sensitivity_rows[0]
        reasons.append(
            f"The most sensitive dependency is {top['Dependency']}."
        )

    assumptions = [
        "Dependency graph remains valid during the planning horizon.",
        "Monte Carlo variation captures meaningful uncertainty.",
        "Surface scores accurately represent the current scenario.",
        "Planner output is treated as advisory, not authoritative.",
    ]

    cautions = []

    if dashboard["uncertainty"] == "High":
        cautions.append(
            "High uncertainty indicates the plan may be fragile."
        )

    if sensitivity_rows:
        top = sensitivity_rows[0]
        if top["Influence"] in ["Very High", "High"]:
            cautions.append(
                f"Outcome is highly sensitive to {top['Dependency']}."
            )

    if not cautions:
        cautions.append(
            "No major caution flags detected from current dashboard inputs."
        )

    return {
        "recommendation": dashboard["recommended_strategy"],
        "reasons": reasons,
        "assumptions": assumptions,
        "cautions": cautions,
    }