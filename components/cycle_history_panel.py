import pandas as pd
import streamlit as st

from engines.cycle_history import load_cycle_history


def render_cycle_history_panel():
    st.markdown("---")
    st.header("Cycle History")

    history = load_cycle_history()

    if not history:
        st.info("No cycle history available yet.")
        return []

    st.dataframe(
        pd.DataFrame(history),
        hide_index=True,
        width="stretch",
    )

    latest = history[0]

    st.markdown("### Latest Cycle State")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Completion",
        f"{latest['Completion']}%",
    )

    c2.metric(
        "Stages Complete",
        latest["Stages Complete"],
    )

    c3.metric(
        "Priority",
        latest["Cycle Priority"],
    )

    return history