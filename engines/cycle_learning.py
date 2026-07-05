def build_cycle_learning(
    cycle_history,
    cycle_trends,
):
    lessons = []

    if not cycle_history:
        return {
            "lessons": [
                "No cycle history available for learning yet."
            ],
            "cycle_maturity": "Unknown",
        }

    if cycle_trends.get("trend") == "Improving":
        lessons.append(
            "Decision cycle completion is improving over time."
        )
    elif cycle_trends.get("trend") == "Declining":
        lessons.append(
            "Decision cycle completion is declining and should be reviewed."
        )
    else:
        lessons.append(
            "Decision cycle completion appears stable."
        )

    average_completion = cycle_trends.get(
        "average_completion",
        0,
    )

    if average_completion >= 90:
        cycle_maturity = "Mature"
        lessons.append(
            "Cycle structure is consistently complete."
        )
    elif average_completion >= 70:
        cycle_maturity = "Developing"
        lessons.append(
            "Cycle structure is mostly present but still improving."
        )
    else:
        cycle_maturity = "Fragile"
        lessons.append(
            "Cycle structure is incomplete or inconsistent."
        )

    dominant_priority = cycle_trends.get(
        "dominant_priority",
        "Unknown",
    )

    lessons.append(
        f"Most common cycle priority is {dominant_priority}."
    )

    return {
        "lessons": lessons,
        "cycle_maturity": cycle_maturity,
    }