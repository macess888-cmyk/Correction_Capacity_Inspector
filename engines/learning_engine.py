from collections import Counter


def build_learning_summary(
    history,
):
    if not history:
        return {
            "successful_strategy": "Unknown",
            "successful_intervention": "Unknown",
            "average_gain": 0,
            "lessons": [],
        }

    strategies = [
        item.get(
            "Recommended Strategy",
            "Unknown",
        )
        for item in history
    ]

    interventions = [
        item.get(
            "Primary Intervention",
            "Unknown",
        )
        for item in history
    ]

    gains = [
        item.get(
            "Projected Gain",
            0,
        )
        for item in history
    ]

    best_strategy = Counter(strategies).most_common(1)[0][0]

    best_intervention = Counter(interventions).most_common(1)[0][0]

    average_gain = round(
        sum(gains) / len(gains),
        2,
    )

    lessons = []

    if average_gain >= 5:
        lessons.append(
            "Planner consistently finds high-value interventions."
        )

    if best_intervention != "Unknown":
        lessons.append(
            f"{best_intervention} frequently appears in successful decisions."
        )

    if len(set(strategies)) > 1:
        lessons.append(
            "Multiple strategies have been explored."
        )

    if not lessons:
        lessons.append(
            "Insufficient history for generalized learning."
        )

    return {
        "successful_strategy": best_strategy,
        "successful_intervention": best_intervention,
        "average_gain": average_gain,
        "lessons": lessons,
    }