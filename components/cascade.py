"""
Cascade Engine

Propagates intervention effects through the
weighted dependency graph.
"""

from components.dependency_engine import DEPENDENCIES


def simulate_cascade(scores, starting_surface, improvement):
    """
    scores:
        dict of surface -> score

    starting_surface:
        surface receiving intervention

    improvement:
        initial increase

    returns:
        projected scores
    """

    projected = scores.copy()

    visited = set()

    def propagate(surface, delta):

        if surface in visited:
            return

        visited.add(surface)

        projected[surface] = min(
            5,
            projected[surface] + delta
        )

        for child, weight in DEPENDENCIES.get(surface, {}).items():

            child_delta = delta * weight

            propagate(child, child_delta)

    propagate(starting_surface, improvement)

    return projected