def classify_influence(score):
    if score >= 0.80:
        return "Very High"
    elif score >= 0.60:
        return "High"
    elif score >= 0.40:
        return "Medium"
    elif score >= 0.20:
        return "Low"
    else:
        return "Very Low"


def analyze_sensitivity(
    dependency_graph,
    monte_carlo_result,
):
    sensitivity_rows = []

    monte_sensitivity = (
        monte_carlo_result.get("sensitivity", {})
        if monte_carlo_result
        else {}
    )

    for source, targets in dependency_graph.items():

        for target, weight in targets.items():

            monte_weight = monte_sensitivity.get(
                target,
                weight,
            )

            sensitivity_score = (
                weight * 0.70
                + monte_weight * 0.30
            )

            sensitivity_rows.append(
                {
                    "Dependency": f"{source} → {target}",
                    "Source": source,
                    "Target": target,
                    "Base Weight": round(weight, 3),
                    "Monte Carlo Weight": round(monte_weight, 3),
                    "Sensitivity": round(sensitivity_score, 3),
                    "Influence": classify_influence(
                        sensitivity_score
                    ),
                }
            )

    sensitivity_rows.sort(
        key=lambda row: row["Sensitivity"],
        reverse=True,
    )

    return sensitivity_rows