import streamlit as st

from engines.cycle_trends import analyze_cycle_trends


def render_cycle_trends_panel(cycle_history):
    st.markdown("---")
    st.header("Cycle Trends")

    trends = analyze_cycle_trends(cycle_history)

    if trends["count"] == 0:
        st.info("No cycle trend data available yet.")
        return trends

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Completion",
        f"{trends['average_completion']}%",
    )

    c2.metric(
        "Latest Completion",
        f"{trends['latest_completion']}%",
    )

    c3.metric(
        "Cycle Trend",
        trends["trend"],
    )

    st.markdown("### Dominant Cycle Priority")

    st.write(trends["dominant_priority"])

    return trends