import streamlit as st

from utils.snapshots import list_snapshots, load_snapshot


def run_recovery_engine():

    st.title("Recovery Intelligence Engine")
    st.subheader("From Pattern Recognition to Recovery Planning")

    st.markdown("---")

    snapshots = list_snapshots()

    if snapshots:
        selected_snapshot = st.selectbox(
            "Load Saved Snapshot",
            ["Manual Entry"] + snapshots
        )
    else:
        selected_snapshot = "Manual Entry"

    if selected_snapshot != "Manual Entry":
        data = load_snapshot(selected_snapshot)

        score = data.get("score", 18)
        system = data.get("system", "UNKNOWN")
        state = data.get("state", "UNKNOWN")
        patterns = data.get("patterns", [])

        st.info(f"Loaded snapshot: {selected_snapshot}")
        st.write(f"**System:** {system}")
        st.write(f"**State:** {state}")

        if patterns:
            st.markdown("### Detected Patterns")
            for pattern in patterns:
                st.warning(pattern.get("pattern", "UNKNOWN"))
                st.write(pattern.get("description", ""))
    else:
        score = st.slider(
            "Current Correction Capacity",
            0,
            30,
            18
        )

    st.markdown("---")

    st.header("Recovery Corridor")

    if score >= 26:
        corridor = "OPEN"
        explanation = (
            "Recovery capacity remains strong. Multiple intervention pathways exist."
        )
    elif score >= 19:
        corridor = "NARROWING"
        explanation = (
            "Recovery remains possible but intervention windows are shrinking."
        )
    elif score >= 12:
        corridor = "CLOSING"
        explanation = (
            "Recovery capacity is weakening. Immediate intervention should be considered."
        )
    else:
        corridor = "COLLAPSED"
        explanation = (
            "Recovery capacity appears critically degraded."
        )

    st.metric("Correction Score", f"{score} / 30")
    st.metric("Recovery Corridor", corridor)
    st.write(explanation)

    st.markdown("---")

    st.header("Recovery Levers")

    signal = st.checkbox("Improve Signal Visibility")
    evidence = st.checkbox("Strengthen Evidence Integrity")
    decision = st.checkbox("Increase Decision Capacity")
    authority = st.checkbox("Increase Authority")
    time = st.checkbox("Create More Time")
    willingness = st.checkbox("Increase Correction Willingness")

    selected = sum([
        signal,
        evidence,
        decision,
        authority,
        time,
        willingness,
    ])

    st.metric("Selected Recovery Levers", selected)

    projected_score = min(
        30,
        score + selected
    )

    projected_gain = projected_score - score

    st.metric("Projected Recovery Score", f"{projected_score} / 30")
    st.metric("Projected Score Gain", projected_gain)

    st.markdown("---")

    st.header("Recovery Assessment")

    st.write(
        f"Projected movement: {score} → {projected_score}"
    )

    if selected >= 5:
        st.success(
            "Strong recovery plan. Multiple intervention surfaces are being strengthened."
        )
    elif selected >= 3:
        st.info(
            "Moderate recovery plan. Several intervention pathways exist."
        )
    elif selected >= 1:
        st.warning(
            "Limited recovery plan. Additional intervention surfaces should be considered."
        )
    else:
        st.error(
            "No recovery strategy selected."
        )

    st.markdown("---")

    st.header("Recovery Summary")

    st.write(
        "Recovery intelligence focuses on identifying which intervention "
        "surfaces remain available before correction capacity collapses."
    )