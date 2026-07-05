import streamlit as st

from engines.decision_quality import calculate_decision_quality


def render_decision_quality_panel(history):
    st.markdown("---")
    st.header("Decision Quality")

    quality = calculate_decision_quality(history)

    if quality["quality_state"] == "Unknown":
        st.info("No decision quality data available yet.")
        return quality

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Quality Score",
        quality["quality_score"],
    )

    c2.metric(
        "Quality State",
        quality["quality_state"],
    )

    c3.metric(
        "Gain Trend",
        quality["gain_trend"],
    )

    st.markdown("### Quality Interpretation")

    st.write(
        f"**Uncertainty State:** {quality['uncertainty_state']}"
    )

    return quality