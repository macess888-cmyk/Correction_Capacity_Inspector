def analyze_cycle_trends(cycle_history):
    if not cycle_history:
        return {
            "count": 0,
            "average_completion": 0,
            "dominant_priority": "Unknown",
            "latest_completion": 0,
            "trend": "Unknown",
        }

    completions = [
        item.get("Completion", 0)
        for item in cycle_history
    ]

    priorities = {}

    for item in cycle_history:
        priority = item.get("Cycle Priority", "Unknown")
        priorities[priority] = priorities.get(priority, 0) + 1

    dominant_priority = max(
        priorities,
        key=priorities.get,
    )

    latest_completion = completions[0]
    oldest_completion = completions[-1]

    if latest_completion > oldest_completion:
        trend = "Improving"
    elif latest_completion < oldest_completion:
        trend = "Declining"
    else:
        trend = "Stable"

    return {
        "count": len(cycle_history),
        "average_completion": round(
            sum(completions) / len(completions),
            2,
        ),
        "dominant_priority": dominant_priority,
        "latest_completion": latest_completion,
        "trend": trend,
    }