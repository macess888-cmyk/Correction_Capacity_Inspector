import streamlit as st

from engines.learning_engine import (
    build_learning_summary,
)


def render_learning_panel(
    history,
):
    st.markdown("---")
    st.header("Learning Engine")

    learning = build_learning_summary(
        history,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Most Successful Strategy",
        learning["successful_strategy"],
    )

    c2.metric(
        "Most Successful Intervention",
        learning["successful_intervention"],
    )

    c3.metric(
        "Average Historical Gain",
        f"+{learning['average_gain']}",
    )

    st.markdown("### Learned Patterns")

    for lesson in learning["lessons"]:
        st.success(lesson)

    return learning