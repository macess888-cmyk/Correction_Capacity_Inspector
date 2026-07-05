import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.snapshots import (
    list_snapshots,
    load_snapshot,
)


def run_timeline_engine():

    st.title("Correction Capacity Timeline")
    st.subheader("Observe how correction capacity changes over time")

    snapshots = list_snapshots()

    if not snapshots:
        st.warning("No snapshots found.")
        return

    rows = []

    for file in snapshots:

        data = load_snapshot(file)

        rows.append(
            {
                "Timestamp": data.get("timestamp", ""),
                "System": data.get("system", ""),
                "Score": data.get("score", 0),
                "Failure Risk": data.get("failure_risk", 0),
                "State": data.get("state", ""),
                "Quadrant": data.get("quadrant", ""),
            }
        )

    df = pd.DataFrame(rows)

    if "Timestamp" in df.columns:
        df = df.sort_values("Timestamp")

    st.markdown("---")
    st.header("Snapshot Timeline")

    st.dataframe(
        df,
        width="stretch"
    )

    st.markdown("---")
    st.header("Correction Capacity Trend")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Score"],
            mode="lines+markers",
            name="Correction Score",
        )
    )

    fig.update_layout(
        title="Correction Capacity Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Correction Score",
        yaxis=dict(range=[0, 30]),
        height=450,
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="timeline_score_chart",
    )

    st.markdown("---")
    st.header("Failure Risk Trend")

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Failure Risk"],
            mode="lines+markers",
            name="Failure Risk",
        )
    )

    fig2.update_layout(
        title="Failure Risk Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Failure Risk",
        yaxis=dict(range=[0, 30]),
        height=450,
    )

    st.plotly_chart(
        fig2,
        width="stretch",
        key="timeline_risk_chart",
    )

    st.markdown("---")
    st.header("Correction vs Failure")

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Score"],
            mode="lines+markers",
            name="Correction Capacity",
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Failure Risk"],
            mode="lines+markers",
            name="Failure Risk",
        )
    )

    fig3.update_layout(
        title="Correction Capacity vs Failure Risk",
        xaxis_title="Timestamp",
        yaxis_title="Score",
        yaxis=dict(range=[0, 30]),
        height=500,
    )

    st.plotly_chart(
        fig3,
        width="stretch",
        key="timeline_overlay_chart",
    )

    st.markdown("---")
    st.header("Timeline Summary")

    latest = df.iloc[-1]

    st.write(f"**Latest System:** {latest['System']}")
    st.write(f"**Latest Score:** {latest['Score']} / 30")
    st.write(f"**Latest Failure Risk:** {latest['Failure Risk']} / 30")
    st.write(f"**Latest State:** {latest['State']}")
    st.write(f"**Latest Quadrant:** {latest['Quadrant']}")