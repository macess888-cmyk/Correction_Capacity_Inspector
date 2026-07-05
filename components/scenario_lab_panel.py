import pandas as pd
import streamlit as st


def render_scenario_lab_panel(
    scenarios,
):
    st.markdown("---")
    st.header("Scenario Laboratory")

    if not scenarios:
        st.info("No scenarios available.")
        return

    rows = []

    for scenario in scenarios:
        planner = scenario.planner_result
        monte = scenario.monte_carlo_result

        rows.append(
            {
                "Scenario": scenario.name,
                "Projected Score": planner.final_score if planner else None,
                "Planner Gain": planner.total_gain if planner else None,
                "Monte Carlo Avg": (
                    monte["average_gain"] if monte else None
                ),
                "Best Case": (
                    monte["best_gain"] if monte else None
                ),
                "Worst Case": (
                    monte["worst_gain"] if monte else None
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
    )