from components.decision_dashboard_panel import (
    render_decision_dashboard_panel,
)
from components.recommendation_rationale_panel import (
    render_recommendation_rationale_panel,
)
from components.scenario_lab_panel import render_scenario_lab_panel
from components.strategy_comparison_panel import (
    render_strategy_comparison_panel,
)
from components.decision_package_viewer_panel import (
    render_decision_package_viewer_panel,
)


def run_decision_intelligence_pipeline(
    plan,
    monte_result,
    sensitivity_rows,
    active_scenarios,
):
    dashboard = render_decision_dashboard_panel(
        plan,
        monte_result,
        sensitivity_rows,
        active_scenarios,
    )

    rationale = render_recommendation_rationale_panel(
        dashboard,
        plan,
        monte_result,
        sensitivity_rows,
    )

    render_scenario_lab_panel(active_scenarios)

    render_strategy_comparison_panel(active_scenarios)

    render_decision_package_viewer_panel()

    return {
        "dashboard": dashboard,
        "rationale": rationale,
    }