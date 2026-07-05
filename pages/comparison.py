import streamlit as st
import pandas as pd

from utils.snapshots import list_snapshots, load_snapshot


def run_case_comparison():
    st.title("Case Comparison Engine")
    st.subheader("Compare saved correction-capacity snapshots")

    snapshots = list_snapshots()

    if len(snapshots) < 2:
        st.warning("Need at least two saved snapshots in the snapshots folder.")
        return

    col_a, col_b = st.columns(2)

    with col_a:
        file_a = st.selectbox("Snapshot A", snapshots, key="snapshot_a")
        case_a = load_snapshot(file_a)

    with col_b:
        file_b = st.selectbox("Snapshot B", snapshots, key="snapshot_b")
        case_b = load_snapshot(file_b)

    a_score = case_a.get("score", 0)
    b_score = case_b.get("score", 0)

    a_risk = case_a.get("failure_risk", 0)
    b_risk = case_b.get("failure_risk", 0)

    score_delta = b_score - a_score
    risk_delta = b_risk - a_risk

    st.markdown("---")
    st.header("Comparison Result")

    st.metric("Snapshot A Score", f"{a_score} / 30")
    st.metric("Snapshot B Score", f"{b_score} / 30")
    st.metric("Correction Capacity Δ", score_delta)
    st.metric("Failure Risk Δ", risk_delta)

    if score_delta > 0 and risk_delta < 0:
        st.success("Trajectory improved. Correction capacity increased and failure risk decreased.")
    elif score_delta < 0 and risk_delta > 0:
        st.error("Trajectory degraded. Correction capacity decreased and failure risk increased.")
    else:
        st.warning("Mixed or stable movement. Review deltas before concluding.")

    st.markdown("### Delta Breakdown")

    fields = [
        "signal",
        "evidence",
        "decision",
        "authority",
        "time",
        "willingness",
    ]

    rows = []

    for field in fields:
        a_val = case_a.get(field, 0)
        b_val = case_b.get(field, 0)

        rows.append(
            {
                "Field": field,
                "Snapshot A": a_val,
                "Snapshot B": b_val,
                "Delta": b_val - a_val,
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        width="stretch"
    )

    st.markdown("### Pattern Comparison")

    a_patterns = case_a.get("patterns", [])
    b_patterns = case_b.get("patterns", [])

    st.write("**Snapshot A Patterns**")

    if a_patterns:
        for pattern in a_patterns:
            st.warning(pattern.get("pattern", "UNKNOWN"))
            st.write(pattern.get("description", ""))
    else:
        st.success("No known patterns detected.")

    st.write("**Snapshot B Patterns**")

    if b_patterns:
        for pattern in b_patterns:
            st.warning(pattern.get("pattern", "UNKNOWN"))
            st.write(pattern.get("description", ""))
    else:
        st.success("No known patterns detected.")

    st.markdown("### Pattern Movement")

    a_pattern_names = {
        pattern.get("pattern", "UNKNOWN")
        for pattern in a_patterns
    }

    b_pattern_names = {
        pattern.get("pattern", "UNKNOWN")
        for pattern in b_patterns
    }

    appeared = b_pattern_names - a_pattern_names
    disappeared = a_pattern_names - b_pattern_names
    persisted = a_pattern_names & b_pattern_names

    if appeared:
        st.error("Patterns appeared:")
        for name in appeared:
            st.write(f"- {name}")

    if disappeared:
        st.success("Patterns disappeared:")
        for name in disappeared:
            st.write(f"- {name}")

    if persisted:
        st.warning("Patterns persisted:")
        for name in persisted:
            st.write(f"- {name}")

    if not appeared and not disappeared and not persisted:
        st.info("No pattern movement detected.")

    st.markdown("### Snapshot A")
    st.json(case_a)

    st.markdown("### Snapshot B")
    st.json(case_b)