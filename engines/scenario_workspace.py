import streamlit as st


def initialize_workspace():
    if "scenario_workspace" not in st.session_state:
        st.session_state["scenario_workspace"] = []


def add_scenario(scenario):
    initialize_workspace()

    existing_names = [
        item.name
        for item in st.session_state["scenario_workspace"]
    ]

    if scenario.name in existing_names:
        suffix = len(existing_names) + 1
        scenario.name = f"{scenario.name} {suffix}"

    st.session_state["scenario_workspace"].append(scenario)


def get_scenarios():
    initialize_workspace()
    return st.session_state["scenario_workspace"]


def clear_scenarios():
    st.session_state["scenario_workspace"] = []