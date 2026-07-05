import streamlit as st

from engines.scenario_workspace import (
    add_scenario,
    clear_scenarios,
    get_scenarios,
)


def render_scenario_workspace_panel(
    current_scenario,
):
    st.markdown("---")
    st.header("Scenario Workspace")

    scenario_name = st.text_input(
        "Scenario Name",
        value=current_scenario.name,
        key="scenario_workspace_name",
    )

    current_scenario.name = scenario_name

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Add Current Scenario"):
            add_scenario(current_scenario)
            st.success(
                f"Added scenario: {current_scenario.name}"
            )

    with c2:
        if st.button("Clear Workspace"):
            clear_scenarios()
            st.warning("Scenario workspace cleared.")

    scenarios = get_scenarios()

    st.markdown("### Saved Scenarios")

    if scenarios:
        for scenario in scenarios:
            st.write(f"• {scenario.name}")
    else:
        st.info("No saved scenarios yet.")

    return scenarios