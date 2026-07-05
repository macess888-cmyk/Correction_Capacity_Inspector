import streamlit as st
import plotly.graph_objects as go


def render_radar(
    signal,
    evidence,
    decision,
    authority,
    time,
    chart_key="failure_radar",
):
    labels = [
        "Financial Stress",
        "Governance Stress",
        "Evidence Gaps",
        "Decision Errors",
        "Continuity Risk",
    ]

    severity = [
        max(1, 6 - signal),
        max(1, 6 - authority),
        max(1, 6 - evidence),
        max(1, 6 - decision),
        max(1, 6 - time),
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=severity,
            theta=labels,
            fill="toself",
            name="Failure Surface",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
            )
        ),
        showlegend=False,
        height=500,
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key=chart_key,
    )