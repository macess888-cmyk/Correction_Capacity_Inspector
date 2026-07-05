import random
import statistics
from copy import deepcopy


def perturb_dependency_graph(
    dependency_graph,
    variation=0.10,
):
    perturbed = {}

    for source, targets in dependency_graph.items():
        perturbed[source] = {}

        for target, weight in targets.items():
            shift = random.uniform(
                -variation,
                variation,
            )

            new_weight = weight + shift
            new_weight = max(0.0, min(1.0, new_weight))

            perturbed[source][target] = new_weight

    return perturbed


def simulate_single_cascade(
    scores,
    dependency_graph,
    intervention_surface,
    improvement=1.0,
):
    state = deepcopy(scores)

    before_total = sum(state.values())

    state[intervention_surface] = min(
        5.0,
        state.get(intervention_surface, 0) + improvement,
    )

    if intervention_surface in dependency_graph:
        for target, weight in dependency_graph[intervention_surface].items():
            state[target] = min(
                5.0,
                state.get(target, 0) + improvement * weight,
            )

    after_total = sum(state.values())

    return {
        "gain": after_total - before_total,
        "final_state": state,
    }


def run_monte_carlo(
    scores,
    dependency_graph,
    intervention_surface,
    iterations=1000,
    variation=0.10,
    improvement=1.0,
):
    gains = []
    sensitivity = {}

    for _ in range(iterations):
        perturbed_graph = perturb_dependency_graph(
            dependency_graph,
            variation,
        )

        result = simulate_single_cascade(
            scores,
            perturbed_graph,
            intervention_surface,
            improvement,
        )

        gains.append(result["gain"])

        for target, weight in perturbed_graph.get(
            intervention_surface,
            {},
        ).items():
            sensitivity[target] = sensitivity.get(target, 0) + weight

    if not gains:
        return {
            "iterations": 0,
            "average_gain": 0,
            "best_gain": 0,
            "worst_gain": 0,
            "confidence_low": 0,
            "confidence_high": 0,
            "sensitivity": {},
        }

    average_gain = statistics.mean(gains)
    sorted_gains = sorted(gains)

    low_index = int(0.025 * len(sorted_gains))
    high_index = int(0.975 * len(sorted_gains)) - 1

    sensitivity = {
        key: round(value / iterations, 3)
        for key, value in sensitivity.items()
    }

    return {
        "iterations": iterations,
        "average_gain": round(average_gain, 3),
        "best_gain": round(max(gains), 3),
        "worst_gain": round(min(gains), 3),
        "confidence_low": round(sorted_gains[low_index], 3),
        "confidence_high": round(sorted_gains[high_index], 3),
        "sensitivity": sensitivity,
    }