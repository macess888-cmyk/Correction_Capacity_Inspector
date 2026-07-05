import streamlit as st

from components.recommendations import recommendation


def render_summary_panel(
    before_scores,
    after_scores,
):
    st.markdown("---")
    st.header("Surface Delta")

    deltas = {}

    for surface, after_value in after_scores.items():
        before_value = before_scores.get(surface, 0)
        deltas[surface] = after_value - before_value

    for surface, delta in deltas.items():
        st.write(f"**{surface}:** {delta:+}")

    st.markdown("---")
    st.header("Largest Improvements")

    positive = [
        (surface, delta)
        for surface, delta in deltas.items()
        if delta > 0
    ]

    positive.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    if positive:
        for surface, delta in positive:
            st.success(f"{surface}: +{delta}")
            st.write(recommendation(surface))
    else:
        st.info("No positive changes.")

    st.markdown("---")
    st.header("Largest Degradations")

    negative = [
        (surface, delta)
        for surface, delta in deltas.items()
        if delta < 0
    ]

    negative.sort(
        key=lambda x: x[1],
    )

    if negative:
        for surface, delta in negative:
            st.error(f"{surface}: {delta}")
            st.write(recommendation(surface))
    else:
        st.success("No degraded surfaces.")

    st.markdown("---")
    st.header("Intervention Summary")

    if negative:
        weakest = negative[0][0]

        st.warning(
            f"Highest-priority intervention: {weakest}"
        )

        st.write(recommendation(weakest))

    elif positive:
        strongest = positive[0][0]

        st.success(
            f"Strongest improvement: {strongest}"
        )

        st.write(recommendation(strongest))

    else:
        st.info(
            "No significant intervention opportunities identified."
        )