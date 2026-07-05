import streamlit as st

from engines.memory_recommendation import (
    build_memory_recommendation,
)


def render_memory_recommendation_panel(memory_insights):
    st.markdown("---")
    st.header("Memory Recommendation Engine")

    result = build_memory_recommendation(memory_insights)

    if result["priority"] == "High":
        st.success(result["recommendation"])
    elif result["priority"] == "Medium":
        st.warning(result["recommendation"])
    else:
        st.info(result["recommendation"])

    st.markdown("### Reason")

    st.write(result["reason"])

    return result