def explain_plan(plan, dependency_graph):
    direct_gain = 0.0
    cascade_gain = 0.0
    affected_surfaces = set()
    dependency_path = []
    strongest_dependency = None

    for step in plan.steps:

        direct_gain += step.improvement
        affected_surfaces.add(step.intervention)

        for effect in step.cascade_trace:

            cascade_gain += effect.get("gain", 0.0)
            affected_surfaces.add(effect.get("to"))

            dependency_path.append(
                {
                    "from": effect.get("from"),
                    "to": effect.get("to"),
                    "weight": effect.get("weight"),
                    "gain": effect.get("gain"),
                }
            )

            if strongest_dependency is None:
                strongest_dependency = effect

            elif effect.get("weight", 0) > strongest_dependency.get("weight", 0):
                strongest_dependency = effect

    total_gain = plan.total_gain

    if cascade_gain > direct_gain:
        summary = "Plan is primarily driven by downstream cascade effects."
    elif direct_gain > cascade_gain:
        summary = "Plan is primarily driven by direct intervention gains."
    else:
        summary = "Plan balances direct gains and cascade effects."

    if total_gain <= 0:
        uncertainty = "High"
    elif len(plan.steps) >= 4:
        uncertainty = "Medium"
    else:
        uncertainty = "Low"

    return {
        "summary": summary,
        "direct_gain": round(direct_gain, 2),
        "cascade_gain": round(cascade_gain, 2),
        "total_gain": round(total_gain, 2),
        "primary_surface": plan.steps[0].intervention if plan.steps else None,
        "affected_surfaces": sorted(
            [surface for surface in affected_surfaces if surface]
        ),
        "dependency_path": dependency_path,
        "strongest_dependency": strongest_dependency,
        "assumptions": [
            "Dependency weights remain stable during the planning horizon.",
            "Cascade propagation is linear.",
            "Current surface scores are accurate.",
            "No external intervention changes the network during simulation.",
            "Planning budget is fully available.",
        ],
        "uncertainty": uncertainty,
        "uncertainty_reasons": [
            "Single deterministic simulation.",
            "Static dependency graph.",
            "No stochastic variation yet.",
            "No confidence interval calculated yet.",
        ],
    }