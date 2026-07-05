import streamlit as st

from engines.cycle_recommendation_memory import (
    build_cycle_recommendation_memory,
)


def render_cycle_recommendation_memory_panel(
    cycle_learning,
    cycle_trends,
):
    st.markdown("---")
    st.header("Cycle Recommendation Memory")

    memory = build_cycle_recommendation_memory(
        cycle_learning,
        cycle_trends,
    )

    if memory["priority"] == "High":
        st.error(memory["recommendation"])
    elif memory["priority"] == "Medium":
        st.warning(memory["recommendation"])
    else:
        st.success(memory["recommendation"])

    st.markdown("### Cycle Memory State")

    st.write(f"**Maturity:** {memory['cycle_maturity']}")
    st.write(f"**Trend:** {memory['cycle_trend']}")
    st.write(f"**Dominant Priority:** {memory['dominant_priority']}")

    return memory