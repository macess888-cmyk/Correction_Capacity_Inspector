import streamlit as st

from engines.decision_cycle import (
    build_decision_cycle,
)


def render_decision_cycle_panel(
    dashboard,
    rationale,
    trends,
    quality,
    learning,
    adaptive,
    memory_recommendation,
):
    st.markdown("---")
    st.header("Decision Cycle")

    cycle = build_decision_cycle(
        dashboard,
        rationale,
        trends,
        quality,
        learning,
        adaptive,
        memory_recommendation,
    )

    stages = [
        "Observation",
        "Reasoning",
        "Planning",
        "Execution",
        "Learning",
    ]

    current = st.selectbox(
        "Decision Cycle Stage",
        stages,
        key="decision_cycle_stage",
    )

    mapping = {
        "Observation": cycle.observation,
        "Reasoning": cycle.reasoning,
        "Planning": cycle.planning,
        "Execution": cycle.execution,
        "Learning": cycle.learning,
    }

    st.json(mapping[current])

    return cycle