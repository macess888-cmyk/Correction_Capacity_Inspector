from components.decision_history_panel import render_decision_history_panel
from components.decision_trends_panel import render_decision_trends_panel
from components.decision_quality_panel import render_decision_quality_panel
from components.learning_panel import render_learning_panel
from components.adaptive_recommendation_panel import (
    render_adaptive_recommendation_panel,
)
from components.decision_memory_panel import render_decision_memory_panel
from components.memory_insight_panel import render_memory_insight_panel
from components.memory_recommendation_panel import (
    render_memory_recommendation_panel,
)


def run_memory_pipeline():
    history = render_decision_history_panel()

    trends = render_decision_trends_panel(history)

    quality = render_decision_quality_panel(history)

    learning = render_learning_panel(history)

    adaptive = render_adaptive_recommendation_panel(
        learning,
        quality,
        trends,
    )

    memory_results = render_decision_memory_panel()

    memory_insights = render_memory_insight_panel(
        memory_results,
    )

    memory_recommendation = render_memory_recommendation_panel(
        memory_insights,
    )

    return {
        "history": history,
        "trends": trends,
        "quality": quality,
        "learning": learning,
        "adaptive": adaptive,
        "memory_recommendation": memory_recommendation,
    }