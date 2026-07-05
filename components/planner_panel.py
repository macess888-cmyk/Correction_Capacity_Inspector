import streamlit as st
import pandas as pd

from engines.planning.intervention_planner import (
    MultiStepInterventionPlanner,
)


def render_planner_panel(
    after_scores,
    weighted_dependency_graph,
):
    st.markdown("---")
    st.header("Strategic Intervention Planner")

    planning_budget = st.slider(
        "Planning Budget",
        1,
        10,
        4,
        key="planning_budget",
    )

    planner = MultiStepInterventionPlanner(
        weighted_dependency_graph
    )

    plan = planner.generate_plan(
        initial_state=after_scores,
        budget=planning_budget,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Initial Score",
        f"{plan.initial_score:.2f} / 30",
    )

    c2.metric(
        "Projected Score",
        f"{plan.final_score:.2f} / 30",
    )

    c3.metric(
        "Projected Gain",
        f"+{plan.total_gain:.2f}",
    )

    st.markdown("### Intervention Sequence")

    if plan.steps:

        for step in plan.steps:

            with st.expander(
                f"Step {step.step_number}: {step.intervention}"
            ):

                st.write(f"Improvement: +{step.improvement}")
                st.write(f"Cost: {step.cost}")

                st.write(
                    f"Score: "
                    f"{step.before_score:.2f}"
                    f" → "
                    f"{step.after_score:.2f}"
                )

                if step.cascade_trace:

                    st.markdown("#### Cascade")

                    for effect in step.cascade_trace:

                        st.write(
                            f"{effect['from']} → "
                            f"{effect['to']} "
                            f"(weight {effect['weight']:.2f}) "
                            f"+{effect['gain']:.2f}"
                        )

    rows = []

    for surface, value in after_scores.items():

        projected = plan.final_state.get(surface, value)

        rows.append(
            {
                "Surface": surface,
                "Current": round(value, 2),
                "Projected": round(projected, 2),
                "Δ": round(projected - value, 2),
            }
        )

    st.markdown("### Final Projected Network")

    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        width="stretch",
    )

    return plan