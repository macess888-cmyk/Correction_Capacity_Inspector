import streamlit as st

from engines.recommendation_rationale import (
    build_recommendation_rationale,
)


def render_recommendation_rationale_panel(
    dashboard,
    plan,
    monte_carlo_result,
    sensitivity_rows,
):
    st.markdown("---")
    st.header("Recommendation Rationale")

    rationale = build_recommendation_rationale(
        dashboard,
        plan,
        monte_carlo_result,
        sensitivity_rows,
    )

    st.success(
        f"Recommended strategy: {rationale['recommendation']}"
    )

    st.markdown("### Why this recommendation?")

    for reason in rationale["reasons"]:
        st.write(f"• {reason}")

    st.markdown("### Assumptions")

    for assumption in rationale["assumptions"]:
        st.write(f"• {assumption}")

    st.markdown("### Cautions")

    for caution in rationale["cautions"]:
        st.warning(caution)

    return rationale