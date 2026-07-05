import streamlit as st

from engines.decision_export import export_decision_package
from engines.strategy_comparison import compare_scenarios


def render_decision_export_panel(
    dashboard,
    rationale,
    active_scenarios,
    decision_cycle=None,
    cycle_completion=None,
    cycle_risks=None,
    cycle_recommendation=None,
):
    st.markdown("---")
    st.header("Decision Export")

    scenario_rows = compare_scenarios(active_scenarios)

    if st.button("Export Decision Package"):
        filename = export_decision_package(
            dashboard,
            rationale,
            scenario_rows,
            cycle=decision_cycle,
            cycle_completion=cycle_completion,
            cycle_risks=cycle_risks,
            cycle_recommendation=cycle_recommendation,
        )

        st.success(
            f"Decision package exported: {filename}"
        )