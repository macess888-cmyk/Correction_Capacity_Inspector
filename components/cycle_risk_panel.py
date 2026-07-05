import pandas as pd
import streamlit as st

from engines.cycle_risk import assess_cycle_risk


def render_cycle_risk_panel(
    cycle_completion,
    dashboard,
    quality,
    adaptive,
):
    st.markdown("---")
    st.header("Cycle Risk Assessment")

    risks = assess_cycle_risk(
        cycle_completion,
        dashboard,
        quality,
        adaptive,
    )

    st.dataframe(
        pd.DataFrame(risks),
        hide_index=True,
        width="stretch",
    )

    highest = risks[0]

    if highest["severity"] == "High":
        st.error(highest["risk"])
    elif highest["severity"] == "Medium":
        st.warning(highest["risk"])
    else:
        st.success(highest["risk"])

    return risks