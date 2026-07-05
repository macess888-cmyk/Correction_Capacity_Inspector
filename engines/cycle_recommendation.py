def build_cycle_recommendation(cycle_risks):
    if not cycle_risks:
        return {
            "recommendation": "Continue normal decision cycle monitoring.",
            "priority": "Low",
            "reason": "No cycle risks were detected.",
        }

    highest = cycle_risks[0]

    if highest["severity"] == "High":
        return {
            "recommendation": (
                "Address the highest-risk cycle issue before relying on the recommendation."
            ),
            "priority": "High",
            "reason": highest["reason"],
        }

    if highest["severity"] == "Medium":
        return {
            "recommendation": (
                "Review the medium-risk issue before finalizing the decision package."
            ),
            "priority": "Medium",
            "reason": highest["reason"],
        }

    return {
        "recommendation": "Cycle appears stable. Continue with decision export and monitoring.",
        "priority": "Low",
        "reason": highest["reason"],
    }