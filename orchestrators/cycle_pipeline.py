from components.cycle_history_panel import render_cycle_history_panel
from components.cycle_trends_panel import render_cycle_trends_panel
from components.cycle_learning_panel import render_cycle_learning_panel
from components.cycle_recommendation_memory_panel import (
    render_cycle_recommendation_memory_panel,
)
from components.decision_cycle_panel import render_decision_cycle_panel
from components.cycle_completion_panel import render_cycle_completion_panel
from components.cycle_risk_panel import render_cycle_risk_panel
from components.cycle_recommendation_panel import (
    render_cycle_recommendation_panel,
)


def run_cycle_pipeline(
    dashboard,
    rationale,
    trends,
    quality,
    learning,
    adaptive,
    memory_recommendation,
):
    cycle_history = render_cycle_history_panel()

    cycle_trends = render_cycle_trends_panel(
        cycle_history,
    )

    cycle_learning = render_cycle_learning_panel(
        cycle_history,
        cycle_trends,
    )

    cycle_recommendation_memory = render_cycle_recommendation_memory_panel(
        cycle_learning,
        cycle_trends,
    )

    decision_cycle = render_decision_cycle_panel(
        dashboard,
        rationale,
        trends,
        quality,
        learning,
        adaptive,
        memory_recommendation,
    )

    cycle_completion = render_cycle_completion_panel(
        decision_cycle,
    )

    cycle_risks = render_cycle_risk_panel(
        cycle_completion,
        dashboard,
        quality,
        adaptive,
    )

    cycle_recommendation = render_cycle_recommendation_panel(
        cycle_risks,
    )

    return {
        "cycle_history": cycle_history,
        "cycle_trends": cycle_trends,
        "cycle_learning": cycle_learning,
        "cycle_recommendation_memory": cycle_recommendation_memory,
        "decision_cycle": decision_cycle,
        "cycle_completion": cycle_completion,
        "cycle_risks": cycle_risks,
        "cycle_recommendation": cycle_recommendation,
    }