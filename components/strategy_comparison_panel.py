import pandas as pd
import streamlit as st

from engines.strategy_comparison import compare_scenarios


def render_strategy_comparison_panel(scenarios):
    st.markdown("---")
    st.header("Strategy Comparison Engine")

    if not scenarios:
        st.info("No scenarios available for comparison.")
        return

    ranked = compare_scenarios(scenarios)

    if not ranked:
        st.info("No ranked strategies available.")
        return

    st.markdown("### Ranked Strategies")

    rows = []

    for item in ranked:
        rows.append(
            {
                "Rank": item["Rank"],
                "Scenario": item["Scenario"],
                "Planner Gain": item["Planner Gain"],
                "Monte Carlo Avg": item["Monte Carlo Avg"],
                "Worst Case": item["Worst Case"],
                "Confidence": f"{item['Confidence']}%",
                "Stability": item["Stability"],
                "Decision Score": item["Decision Score"],
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
    )

    winner = ranked[0]

    st.success(
        f"Top-ranked strategy: {winner['Scenario']}"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Decision Score",
        winner["Decision Score"],
    )

    c2.metric(
        "Planner Gain",
        f"+{winner['Planner Gain']:.2f}",
    )

    c3.metric(
        "Confidence",
        f"{winner['Confidence']}%",
    )

    st.markdown("### Strategy Notes")

    if winner["Stability"] == "High":
        st.info("Top strategy appears stable under uncertainty.")
    elif winner["Stability"] == "Medium":
        st.warning("Top strategy has moderate uncertainty.")
    else:
        st.error("Top strategy has high uncertainty.")