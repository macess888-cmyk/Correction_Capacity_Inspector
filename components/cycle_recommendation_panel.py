import streamlit as st

from engines.cycle_recommendation import build_cycle_recommendation


def render_cycle_recommendation_panel(cycle_risks):
    st.markdown("---")
    st.header("Cycle Recommendation")

    result = build_cycle_recommendation(cycle_risks)

    if result["priority"] == "High":
        st.error(result["recommendation"])
    elif result["priority"] == "Medium":
        st.warning(result["recommendation"])
    else:
        st.success(result["recommendation"])

    st.markdown("### Reason")
    st.write(result["reason"])

    return result