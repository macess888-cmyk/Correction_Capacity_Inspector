"""
Intervention Optimizer

Finds the highest-impact intervention
given a limited improvement budget.
"""

from components.cascade import simulate_cascade


def optimize_intervention(scores, budget=3.0):
    """
    scores:
        dict of surface -> score

    budget:
        available intervention points

    Returns:
        ranked intervention options
    """

    options = []

    for surface in scores:

        projected = simulate_cascade(
            scores,
            surface,
            budget
        )

        base_total = sum(scores.values())
        projected_total = sum(projected.values())

        gain = projected_total - base_total

        options.append(
            {
                "surface": surface,
                "gain": round(gain, 2),
                "projected": projected,
            }
        )

    options.sort(
        key=lambda x: x["gain"],
        reverse=True,
    )

    return options