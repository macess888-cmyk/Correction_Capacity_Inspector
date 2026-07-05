from engines.scenario_lab import Scenario

from components.monte_carlo_panel import render_monte_carlo_panel
from components.sensitivity_panel import render_sensitivity_panel
from components.planner_panel import render_planner_panel
from components.constraint_panel import render_constraint_panel
from components.recovery_corridor_panel import render_recovery_corridor_panel
from components.explainability_panel import render_explainability_panel
from components.summary_panel import render_summary_panel
from components.scenario_workspace_panel import (
    render_scenario_workspace_panel,
)


def run_planning_pipeline(
    before_scores,
    after_scores,
    weighted_dependency_graph,
):
    monte_result = render_monte_carlo_panel(
        after_scores,
        weighted_dependency_graph,
    )

    sensitivity_rows = render_sensitivity_panel(
        weighted_dependency_graph,
        monte_result,
    )

    plan = render_planner_panel(
        after_scores,
        weighted_dependency_graph,
    )

    current_scenario = Scenario(
        name="Current Scenario",
        scores=after_scores,
        planner_result=plan,
        monte_carlo_result=monte_result,
    )

    render_constraint_panel(
        plan,
        list(after_scores.keys()),
    )

    render_recovery_corridor_panel(plan)

    render_explainability_panel(
        plan,
        weighted_dependency_graph,
    )

    render_summary_panel(
        before_scores,
        after_scores,
    )

    saved_scenarios = render_scenario_workspace_panel(
        current_scenario,
    )

    active_scenarios = (
        saved_scenarios
        if saved_scenarios
        else [current_scenario]
    )

    return {
        "plan": plan,
        "monte_result": monte_result,
        "sensitivity_rows": sensitivity_rows,
        "current_scenario": current_scenario,
        "active_scenarios": active_scenarios,
    }