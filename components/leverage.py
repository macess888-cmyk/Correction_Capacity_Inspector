"""
Leverage Point Analyzer

Ranks intervention surfaces by weighted downstream influence.
"""

from components.dependency_engine import DEPENDENCIES


def calculate_leverage(scores):
    """
    scores = {
        surface: score
    }

    Returns ranked intervention opportunities.
    """

    leverage = []

    for surface, value in scores.items():

        downstream = DEPENDENCIES.get(surface, {})

        downstream_weight = sum(
            downstream.values()
        )

        weakness_bonus = 5 - value

        leverage_score = (
            downstream_weight * 2
            + weakness_bonus
        )

        leverage.append(
            {
                "surface": surface,
                "current_score": value,
                "downstream": downstream,
                "downstream_weight": downstream_weight,
                "leverage_score": round(leverage_score, 2),
            }
        )

    leverage.sort(
        key=lambda x: x["leverage_score"],
        reverse=True,
    )

    return leverage