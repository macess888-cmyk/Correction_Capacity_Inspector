import streamlit as st

from engines.memory_insight import build_memory_insights


def render_memory_insight_panel(memory_results):
    st.markdown("---")
    st.header("Memory Insight Engine")

    insights = build_memory_insights(memory_results)

    if insights["count"] == 0:
        st.info(insights["insight"])
        return insights

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Matching Memories",
        insights["count"],
    )

    c2.metric(
        "Average Gain",
        f"+{insights['average_gain']}",
    )

    c3.metric(
        "Dominant Uncertainty",
        insights["dominant_uncertainty"],
    )

    st.markdown("### Memory Pattern")

    st.info(insights["insight"])

    st.write(
        f"**Top Strategy:** {insights['top_strategy']}"
    )

    st.write(
        f"**Top Intervention:** {insights['top_intervention']}"
    )

    return insights