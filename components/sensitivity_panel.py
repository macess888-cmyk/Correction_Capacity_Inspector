import pandas as pd
import streamlit as st

from engines.sensitivity_analysis import analyze_sensitivity


def render_sensitivity_panel(
    dependency_graph,
    monte_carlo_result,
):
    st.markdown("---")
    st.header("Sensitivity Analysis Engine")

    rows = analyze_sensitivity(
        dependency_graph,
        monte_carlo_result,
    )

    if not rows:
        st.info("No sensitivity data available.")
        return []

    st.markdown("### Ranked Dependency Sensitivity")

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
    )

    strongest = rows[0]
    weakest = rows[-1]

    c1, c2 = st.columns(2)

    c1.metric(
        "Most Sensitive Dependency",
        strongest["Dependency"],
    )

    c2.metric(
        "Sensitivity Score",
        strongest["Sensitivity"],
    )

    st.markdown("### Interpretation")

    st.info(
        f"The most sensitive dependency is "
        f"{strongest['Dependency']} "
        f"with {strongest['Influence']} influence."
    )

    st.caption(
        f"Lowest sensitivity observed: "
        f"{weakest['Dependency']} "
        f"({weakest['Sensitivity']})."
    )

    return rows