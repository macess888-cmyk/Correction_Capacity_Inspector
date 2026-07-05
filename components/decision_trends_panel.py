import pandas as pd
import streamlit as st

from engines.decision_trends import analyze_decision_trends


def render_decision_trends_panel(history):
    st.markdown("---")
    st.header("Decision Trends")

    trends = analyze_decision_trends(history)

    if trends["count"] == 0:
        st.info("No decision trend data available yet.")
        return trends

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Decision Count",
        trends["count"],
    )

    c2.metric(
        "Average Gain",
        f"+{trends['average_gain']}",
    )

    c3.metric(
        "Best Gain",
        f"+{trends['best_gain']}",
    )

    st.markdown("### Trend Summary")

    st.write(
        f"**Best Strategy:** {trends['best_strategy']}"
    )

    st.write(
        f"**Most Common Intervention:** "
        f"{trends['most_common_intervention']}"
    )

    st.markdown("### Uncertainty Distribution")

    uncertainty_rows = [
        {
            "Uncertainty": key,
            "Count": value,
        }
        for key, value in trends["uncertainty_counts"].items()
    ]

    if uncertainty_rows:
        st.dataframe(
            pd.DataFrame(uncertainty_rows),
            hide_index=True,
            width="stretch",
        )

    return trends