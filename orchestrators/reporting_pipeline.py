from components.decision_export_panel import render_decision_export_panel


def run_reporting_pipeline(
    dashboard,
    rationale,
    active_scenarios,
    decision_cycle,
    cycle_completion,
    cycle_risks,
    cycle_recommendation,
):
    render_decision_export_panel(
        dashboard,
        rationale,
        active_scenarios,
        decision_cycle=decision_cycle,
        cycle_completion=cycle_completion,
        cycle_risks=cycle_risks,
        cycle_recommendation=cycle_recommendation,
    )