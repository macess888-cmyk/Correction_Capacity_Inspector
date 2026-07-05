import streamlit as st

from engines.decision_dashboard import build_decision_dashboard


def render_decision_dashboard_panel(
    plan,
    monte_carlo_result,
    sensitivity_rows,
    active_scenarios,
):
    st.markdown("---")
    st.header("Decision Dashboard")

    dashboard = build_decision_dashboard(
        plan,
        monte_carlo_result,
        sensitivity_rows,
        active_scenarios,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Recommended Strategy",
        dashboard["recommended_strategy"],
    )

    c2.metric(
        "Projected Gain",
        f"+{dashboard['projected_gain']:.2f}",
    )

    c3.metric(
        "Monte Carlo Avg",
        f"+{dashboard['monte_carlo_average']:.2f}",
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Uncertainty",
        dashboard["uncertainty"],
    )

    low, high = dashboard["confidence_range"]

    c5.metric(
        "Confidence Range",
        f"{low:.2f} → {high:.2f}",
    )

    c6.metric(
        "Primary Intervention",
        dashboard["primary_intervention"],
    )

    st.markdown("### Key Sensitivity")

    st.info(
        f"{dashboard['most_sensitive_dependency']} "
        f"({dashboard['sensitivity_level']})"
    )

    return dashboard