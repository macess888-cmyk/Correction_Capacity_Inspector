import streamlit as st

from components.scoring import (
    interpret_score,
    risk_state_from_score,
)


def run_analysis_pipeline(
    before_scores,
    after_scores,
):
    before_score = sum(before_scores.values())
    after_score = sum(after_scores.values())

    before_risk, before_risk_state = risk_state_from_score(
        before_score
    )

    after_risk, after_risk_state = risk_state_from_score(
        after_score
    )

    score_delta = after_score - before_score
    risk_delta = after_risk - before_risk

    before_state, before_explanation = interpret_score(
        before_score
    )

    after_state, after_explanation = interpret_score(
        after_score
    )

    st.markdown("---")
    st.header("Simulation Result")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Before Score",
        f"{before_score} / 30",
    )

    c2.metric(
        "After Score",
        f"{after_score} / 30",
    )

    c3.metric(
        "Score Δ",
        score_delta,
    )

    c4.metric(
        "Risk Δ",
        risk_delta,
    )

    st.markdown("### Before")

    st.write(f"**State:** {before_state}")
    st.write(before_explanation)
    st.write(f"Risk State: **{before_risk_state}**")

    st.markdown("### After")

    st.write(f"**State:** {after_state}")
    st.write(after_explanation)
    st.write(f"Risk State: **{after_risk_state}**")

    st.markdown("---")
    st.header("Trajectory Assessment")

    if score_delta > 0 and risk_delta < 0:
        st.success("Projected trajectory improves.")

    elif score_delta < 0 and risk_delta > 0:
        st.error("Projected trajectory degrades.")

    elif score_delta == 0 and risk_delta == 0:
        st.warning("No measurable trajectory change.")

    else:
        st.info("Mixed trajectory movement detected.")

    return {
        "before_score": before_score,
        "after_score": after_score,
        "score_delta": score_delta,
        "risk_delta": risk_delta,
        "before_risk": before_risk,
        "after_risk": after_risk,
        "before_state": before_state,
        "after_state": after_state,
    }