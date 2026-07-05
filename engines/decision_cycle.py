from dataclasses import dataclass


@dataclass
class DecisionCycle:
    observation: dict
    reasoning: dict
    planning: dict
    execution: dict
    learning: dict


def build_decision_cycle(
    dashboard,
    rationale,
    trends,
    quality,
    learning,
    adaptive,
    memory_recommendation,
):
    return DecisionCycle(
        observation={
            "recommended_strategy": dashboard["recommended_strategy"],
            "projected_gain": dashboard["projected_gain"],
        },
        reasoning={
            "rationale": rationale["reasons"],
            "quality": quality,
            "trends": trends,
        },
        planning={
            "adaptive": adaptive,
        },
        execution={
            "memory_recommendation": memory_recommendation,
        },
        learning={
            "learning": learning,
        },
    )