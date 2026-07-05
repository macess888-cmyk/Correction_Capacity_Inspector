import streamlit as st

from engines.cycle_learning import build_cycle_learning


def render_cycle_learning_panel(
    cycle_history,
    cycle_trends,
):
    st.markdown("---")
    st.header("Cycle Learning")

    learning = build_cycle_learning(
        cycle_history,
        cycle_trends,
    )

    st.metric(
        "Cycle Maturity",
        learning["cycle_maturity"],
    )

    st.markdown("### Learned Cycle Patterns")

    for lesson in learning["lessons"]:
        st.write(f"• {lesson}")

    return learning