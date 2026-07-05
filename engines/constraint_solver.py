from dataclasses import dataclass, field


@dataclass
class PlanningConstraints:

    budget: int = 4

    locked_surfaces: set = field(default_factory=set)

    minimum_scores: dict = field(default_factory=dict)

    maximum_scores: dict = field(default_factory=dict)

    protected_surfaces: set = field(default_factory=set)


def validate_plan(
    plan,
    constraints,
):
    violations = []

    if len(plan.steps) > constraints.budget:
        violations.append(
            f"Plan exceeds budget ({constraints.budget})"
        )

    for step in plan.steps:

        surface = step.intervention

        if surface in constraints.locked_surfaces:

            violations.append(
                f"{surface} is locked."
            )

    for surface, minimum in constraints.minimum_scores.items():

        value = plan.final_state.get(surface, 0)

        if value < minimum:

            violations.append(
                f"{surface} below minimum ({minimum})"
            )

    for surface, maximum in constraints.maximum_scores.items():

        value = plan.final_state.get(surface, 0)

        if value > maximum:

            violations.append(
                f"{surface} exceeds maximum ({maximum})"
            )

    for surface in constraints.protected_surfaces:

        initial = plan.initial_state.get(surface, 0)
        final = plan.final_state.get(surface, 0)

        if final < initial:

            violations.append(
                f"{surface} decreased."
            )

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }