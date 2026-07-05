import streamlit as st
from datetime import datetime

from components.scoring import (
    interpret_score,
    risk_state_from_score,
    trajectory_quadrant,
    preservation_risk_from_choice,
)

from components.charts import render_radar
from components.interventions import intervention_priority
from components.patterns import detect_patterns
from utils.snapshots import save_snapshot


def run_single_inspection():
    st.title("Correction Capacity Inspector")
    st.subheader("Seeing the pothole ≠ Filling the pothole")

    st.markdown("---")

    st.header("System Information")

    system_name = st.text_input("System Name")
    problem = st.text_area("Describe the visible problem")

    st.markdown("---")

    st.header("Correction Capacity")

    col1, col2 = st.columns(2)

    with col1:
        signal = st.slider("Signal Visibility", 0, 5, 3)
        evidence = st.slider("Evidence Integrity", 0, 5, 3)
        decision = st.slider("Decision Capacity", 0, 5, 3)

    with col2:
        authority = st.slider("Authority To Act", 0, 5, 3)
        time = st.slider("Remaining Time", 0, 5, 3)
        willingness = st.slider("Correction Willingness", 0, 5, 3)

    score = signal + evidence + decision + authority + time + willingness
    max_score = 30

    st.metric("Correction Score", f"{score} / {max_score}")

    st.markdown("---")

    st.header("Interpretation")

    state, explanation = interpret_score(score, max_score)

    st.subheader(state)
    st.write(explanation)

    st.info(
        "Core Question: Do we still have enough information and governance capacity "
        "to alter the trajectory?"
    )

    st.markdown("---")

    st.header("Pattern Intelligence")

    pattern_matches = detect_patterns(
        signal,
        evidence,
        decision,
        authority,
        time,
        willingness,
    )

    if pattern_matches:
        for match in pattern_matches:
            st.warning(f"Detected Pattern: {match['pattern']}")
            st.write(match["description"])
    else:
        st.success("No known governability failure pattern detected.")

    st.markdown("---")

    st.header("Cost Export Map")

    who_affected = st.text_area("Who is affected if nothing changes?")
    who_authority = st.text_area("Who has authority to correct it?")
    cost_no_change = st.text_area("Who pays the cost if nothing changes?")
    cost_correction = st.text_area("Who pays the cost if correction happens?")
    blockers = st.text_area("What blocks correction?")

    st.markdown("---")

    st.header("Recursive Failure Loop")

    st.code(
        """
Financial Stress
    ↓
Governance Stress
    ↓
Evidence Gaps
    ↓
Decision Errors
    ↓
Continuity Risk
    ↓
More Financial Stress
        """,
        language="text"
    )

    st.markdown("---")

    st.header("Trajectory Alterability")

    capacity_score = signal + evidence + decision + authority + time
    willingness_score = willingness

    quadrant, quadrant_meaning = trajectory_quadrant(
        capacity_score,
        willingness_score
    )

    st.subheader(quadrant)
    st.write(quadrant_meaning)

    st.markdown("---")

    st.header("Pattern Diagnosis")

    diagnosis = {
        "Blindness Risk": signal,
        "Evidence Risk": evidence,
        "Decision Risk": decision,
        "Authority Risk": authority,
        "Time Risk": time,
        "Willingness Risk": willingness,
    }

    for label, value in diagnosis.items():
        if value >= 4:
            status = "STABLE"
        elif value >= 2:
            status = "WEAKENING"
        else:
            status = "CRITICAL"

        st.write(f"**{label}:** {status}")
        st.progress(value / 5)

    st.markdown("### Diagnostic Questions")

    st.write(f"**Can the system see the problem?** {'YES' if signal >= 3 else 'NO / WEAK'}")
    st.write(f"**Can the system prove what is happening?** {'YES' if evidence >= 3 else 'NO / WEAK'}")
    st.write(f"**Can the system decide?** {'YES' if decision >= 3 else 'NO / WEAK'}")
    st.write(f"**Can the system act?** {'YES' if authority >= 3 else 'NO / WEAK'}")
    st.write(f"**Will the system act?** {'YES' if willingness >= 3 else 'NO / WEAK'}")
    st.write(f"**Is there still time?** {'YES' if time >= 3 else 'NO / WEAK'}")

    st.markdown("---")

    st.header("Compounding Failure Topology")
    render_radar(signal, evidence, decision, authority, time)

    st.markdown("### Catastrophic Failure Risk")

    failure_risk, risk_state = risk_state_from_score(score, max_score)

    st.metric("Failure Risk Score", f"{failure_risk} / {max_score}")
    st.write(f"Risk State: **{risk_state}**")

    st.markdown("### Recovery Corridor")

    if score >= 26:
        st.success("Trajectory appears alterable. Correction capacity remains strong.")
    elif score >= 19:
        st.info("Trajectory is still alterable, but intervention windows are narrowing.")
    elif score >= 12:
        st.warning("Recovery window is closing. Compounding dynamics are strengthening.")
    else:
        st.error("Catastrophic trajectory forming. Correction capacity may be collapsing.")

    st.markdown("---")

    st.header("Preservation vs Correction Inspector")

    benefit_no_change = st.text_area("Who benefits if nothing changes?")
    burden_no_change = st.text_area("Who absorbs the burden if nothing changes?")
    lose_power = st.text_area("Who loses power if correction happens?")
    gain_safety = st.text_area("Who gains safety if correction happens?")

    preservation_choice = st.selectbox(
        "Is the system choosing preservation over correction?",
        [
            "UNKNOWN",
            "NO",
            "PARTIALLY",
            "YES"
        ]
    )

    preservation_risk = preservation_risk_from_choice(preservation_choice)

    st.markdown("### Pattern Assessment")

    st.write(f"**Preservation Over Correction Risk:** {preservation_risk}")

    direction = st.selectbox(
        "Burden Direction",
        [
            "UNKNOWN",
            "UPWARD",
            "DOWNWARD",
            "LATERAL"
        ]
    )

    cost_export = st.selectbox(
        "Cost Export Detected?",
        [
            "UNKNOWN",
            "NO",
            "YES"
        ]
    )

    st.write(f"**Cost Export Detected:** {cost_export}")
    st.write(f"**Burden Direction:** {direction}")

    st.markdown("---")

    st.header("Intervention Planner")

    recommendations = intervention_priority(
        signal,
        evidence,
        decision,
        authority,
        time,
        willingness,
    )

    st.markdown("### Priority Ranking")

    for item in recommendations:
        st.write(
            f"**{item['priority']}** — "
            f"{item['surface']} "
            f"(score: {item['score']} / 5)"
        )

    weakest = recommendations[0]

    st.info(
        f"Suggested first intervention surface: "
        f"{weakest['surface']}"
    )

    st.header("Next Small Correction")

    next_action = st.text_area(
        "What is the smallest intervention that could alter the trajectory?"
    )

    if st.button("Save Snapshot"):
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "system": system_name,
            "problem": problem,
            "score": score,
            "state": state,
            "quadrant": quadrant,
            "failure_risk": failure_risk,
            "risk_state": risk_state,
            "signal": signal,
            "evidence": evidence,
            "decision": decision,
            "authority": authority,
            "time": time,
            "willingness": willingness,
            "patterns": pattern_matches,
            "preservation_risk": preservation_risk,
            "cost_export": cost_export,
            "burden_direction": direction,
            "next_action": next_action,
        }

        safe_name = system_name.strip().replace(" ", "_") if system_name else "unnamed_system"
        filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        save_snapshot(filename, snapshot)

        st.success(f"Snapshot saved: {filename}")

    if st.button("Generate Observation Summary"):
        st.markdown("## Observation Summary")

        st.write(f"**System:** {system_name if system_name else 'UNKNOWN'}")
        st.write(f"**Visible Problem:** {problem if problem else 'UNKNOWN'}")
        st.write(f"**Correction Score:** {score} / {max_score}")
        st.write(f"**State:** {state}")
        st.write(f"**Trajectory Quadrant:** {quadrant}")
        st.write(f"**Failure Risk:** {failure_risk} / {max_score}")
        st.write(f"**Risk State:** {risk_state}")

        st.write("### Pattern Intelligence")

        if pattern_matches:
            for match in pattern_matches:
                st.write(f"**{match['pattern']}**")
                st.write(match["description"])
        else:
            st.write("No known governability failure pattern detected.")

        st.write("### Core Pattern")
        st.write(
            "The visible failures may not be separate problems. They may be expressions "
            "of one recursive loop affecting correction capacity."
        )

        st.write("### Cost Export")
        st.write(f"**Affected if nothing changes:** {who_affected if who_affected else 'UNKNOWN'}")
        st.write(f"**Authority to correct:** {who_authority if who_authority else 'UNKNOWN'}")
        st.write(f"**Cost if nothing changes:** {cost_no_change if cost_no_change else 'UNKNOWN'}")
        st.write(f"**Cost if correction happens:** {cost_correction if cost_correction else 'UNKNOWN'}")
        st.write(f"**Correction blockers:** {blockers if blockers else 'UNKNOWN'}")

        st.write("### Preservation vs Correction")
        st.write(f"**Preservation Over Correction Risk:** {preservation_risk}")
        st.write(f"**Cost Export Detected:** {cost_export}")
        st.write(f"**Burden Direction:** {direction}")

        st.write(
            f"**Benefiting if nothing changes:** "
            f"{benefit_no_change if benefit_no_change else 'UNKNOWN'}"
        )

        st.write(
            f"**Burden absorbed by:** "
            f"{burden_no_change if burden_no_change else 'UNKNOWN'}"
        )

        st.write(
            f"**Loses power if corrected:** "
            f"{lose_power if lose_power else 'UNKNOWN'}"
        )

        st.write(
            f"**Gains safety if corrected:** "
            f"{gain_safety if gain_safety else 'UNKNOWN'}"
        )

        st.write("### Next Small Correction")
        st.write(next_action if next_action else "UNKNOWN")

        st.warning("UNKNOWN → HOLD")