"""
Weighted Dependency Engine

Models how governability surfaces influence one another.
"""

DEPENDENCIES = {

    "Signal Visibility": {
        "Evidence Integrity": 0.90,
        "Decision Capacity": 0.35,
    },

    "Evidence Integrity": {
        "Decision Capacity": 0.85,
        "Authority To Act": 0.30,
    },

    "Decision Capacity": {
        "Authority To Act": 0.80,
        "Correction Willingness": 0.25,
    },

    "Authority To Act": {
        "Correction Willingness": 0.85,
    },

    "Correction Willingness": {
        "Remaining Time": 0.70,
    },

    "Remaining Time": {},
}


def calculate_dependency_effects(scores):

    influence = {}

    for surface, score in scores.items():

        influence[surface] = {
            "score": score,
            "affects": DEPENDENCIES.get(surface, {}),
        }

    return influence


def weakest_surface(scores):

    return min(
        scores.items(),
        key=lambda x: x[1]
    )


def strongest_surface(scores):

    return max(
        scores.items(),
        key=lambda x: x[1]
    )