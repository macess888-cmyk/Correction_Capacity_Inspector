import pandas as pd
import streamlit as st

from engines.decision_history import load_decision_history


def render_decision_history_panel():
    st.markdown("---")
    st.header("Decision History")

    history = load_decision_history()

    if not history:
        st.info("No decision history available yet.")
        return []

    st.dataframe(
        pd.DataFrame(history),
        hide_index=True,
        width="stretch",
    )

    latest = history[0]

    st.markdown("### Latest Decision")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Strategy",
        latest["Recommended Strategy"],
    )

    c2.metric(
        "Projected Gain",
        f"+{latest['Projected Gain']}",
    )

    c3.metric(
        "Uncertainty",
        latest["Uncertainty"],
    )

    return history