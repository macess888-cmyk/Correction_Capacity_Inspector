import streamlit as st

from engines.constraint_solver import (
    PlanningConstraints,
    validate_plan,
)


def render_constraint_panel(
    plan,
    surfaces,
):
    st.markdown("---")
    st.header("Constraint Solver")

    budget = st.slider(
        "Maximum Planning Steps",
        1,
        10,
        4,
        key="constraint_budget",
    )

    locked = st.multiselect(
        "Locked Surfaces",
        surfaces,
    )

    protected = st.multiselect(
        "Protected Surfaces",
        surfaces,
    )

    minimum_scores = {}

    st.markdown("### Minimum Required Scores")

    for surface in surfaces:

        minimum_scores[surface] = st.slider(
            f"{surface} Minimum",
            0,
            5,
            0,
            key=f"min_{surface}",
        )

    constraints = PlanningConstraints(
        budget=budget,
        locked_surfaces=set(locked),
        protected_surfaces=set(protected),
        minimum_scores=minimum_scores,
    )

    result = validate_plan(
        plan,
        constraints,
    )

    if result["valid"]:

        st.success(
            "Plan satisfies all constraints."
        )

    else:

        st.error(
            "Constraint violations detected."
        )

        for violation in result["violations"]:

            st.write(f"• {violation}")

    return constraints