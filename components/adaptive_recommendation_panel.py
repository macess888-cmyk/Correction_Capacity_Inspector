import streamlit as st

from engines.adaptive_recommendation import (
    build_adaptive_recommendation,
)


def render_adaptive_recommendation_panel(
    learning,
    quality,
    trends,
):
    st.markdown("---")
    st.header("Adaptive Recommendation Engine")

    adaptive = build_adaptive_recommendation(
        learning,
        quality,
        trends,
    )

    if adaptive["priority"] == "High":
        st.error(adaptive["recommendation"])
    elif adaptive["priority"] == "Medium":
        st.warning(adaptive["recommendation"])
    else:
        st.info(adaptive["recommendation"])

    st.markdown("### Why")

    for reason in adaptive["reasons"]:
        st.write(f"• {reason}")

    return adaptive