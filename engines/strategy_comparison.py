def confidence_from_monte_carlo(monte):
    if not monte:
        return 0

    average = monte.get("average_gain", 0)
    low = monte.get("confidence_low", 0)
    high = monte.get("confidence_high", 0)

    spread = high - low

    if average <= 0:
        return 0

    confidence = max(
        0,
        min(
            100,
            100 - (spread / max(average, 0.01)) * 25,
        ),
    )

    return round(confidence, 1)


def stability_from_monte_carlo(monte):
    if not monte:
        return "Unknown"

    low = monte.get("confidence_low", 0)
    high = monte.get("confidence_high", 0)

    spread = high - low

    if spread <= 0.5:
        return "High"
    elif spread <= 1.5:
        return "Medium"
    else:
        return "Low"


def compare_scenarios(scenarios):
    rows = []

    for scenario in scenarios:
        planner = scenario.planner_result
        monte = scenario.monte_carlo_result

        projected_score = planner.final_score if planner else 0
        planner_gain = planner.total_gain if planner else 0
        average_gain = monte.get("average_gain", 0) if monte else 0
        best_gain = monte.get("best_gain", 0) if monte else 0
        worst_gain = monte.get("worst_gain", 0) if monte else 0

        confidence = confidence_from_monte_carlo(monte)
        stability = stability_from_monte_carlo(monte)

        decision_score = (
            planner_gain * 0.40
            + average_gain * 0.35
            + confidence * 0.02
            + worst_gain * 0.25
        )

        rows.append(
            {
                "Scenario": scenario.name,
                "Projected Score": round(projected_score, 2),
                "Planner Gain": round(planner_gain, 2),
                "Monte Carlo Avg": round(average_gain, 2),
                "Best Case": round(best_gain, 2),
                "Worst Case": round(worst_gain, 2),
                "Confidence": confidence,
                "Stability": stability,
                "Decision Score": round(decision_score, 2),
            }
        )

    rows.sort(
        key=lambda item: item["Decision Score"],
        reverse=True,
    )

    for index, row in enumerate(rows, start=1):
        row["Rank"] = index

    return rows