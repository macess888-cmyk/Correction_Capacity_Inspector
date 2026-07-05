import streamlit as st


def run_observation_pipeline():
    st.title("Scenario Simulator")
    st.subheader("Before vs After Correction Capacity Simulation")

    st.markdown(
        "Compare current conditions against a proposed intervention scenario."
    )

    st.markdown("---")

    col_before, col_after = st.columns(2)

    with col_before:
        st.header("Before")

        before_signal = st.slider(
            "Before Signal Visibility",
            0,
            5,
            3,
        )

        before_evidence = st.slider(
            "Before Evidence Integrity",
            0,
            5,
            3,
        )

        before_decision = st.slider(
            "Before Decision Capacity",
            0,
            5,
            3,
        )

        before_authority = st.slider(
            "Before Authority To Act",
            0,
            5,
            3,
        )

        before_time = st.slider(
            "Before Remaining Time",
            0,
            5,
            3,
        )

        before_willingness = st.slider(
            "Before Correction Willingness",
            0,
            5,
            3,
        )

    with col_after:
        st.header("After")

        after_signal = st.slider(
            "After Signal Visibility",
            0,
            5,
            3,
        )

        after_evidence = st.slider(
            "After Evidence Integrity",
            0,
            5,
            3,
        )

        after_decision = st.slider(
            "After Decision Capacity",
            0,
            5,
            3,
        )

        after_authority = st.slider(
            "After Authority To Act",
            0,
            5,
            3,
        )

        after_time = st.slider(
            "After Remaining Time",
            0,
            5,
            3,
        )

        after_willingness = st.slider(
            "After Correction Willingness",
            0,
            5,
            3,
        )

    before_scores = {
        "Signal Visibility": before_signal,
        "Evidence Integrity": before_evidence,
        "Decision Capacity": before_decision,
        "Authority To Act": before_authority,
        "Remaining Time": before_time,
        "Correction Willingness": before_willingness,
    }

    after_scores = {
        "Signal Visibility": after_signal,
        "Evidence Integrity": after_evidence,
        "Decision Capacity": after_decision,
        "Authority To Act": after_authority,
        "Remaining Time": after_time,
        "Correction Willingness": after_willingness,
    }

    return {
        "before_scores": before_scores,
        "after_scores": after_scores,
        "before_values": {
            "signal": before_signal,
            "evidence": before_evidence,
            "decision": before_decision,
            "authority": before_authority,
            "time": before_time,
            "willingness": before_willingness,
        },
        "after_values": {
            "signal": after_signal,
            "evidence": after_evidence,
            "decision": after_decision,
            "authority": after_authority,
            "time": after_time,
            "willingness": after_willingness,
        },
    }
