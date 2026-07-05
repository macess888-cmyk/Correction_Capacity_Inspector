import streamlit as st
import plotly.graph_objects as go


def render_governability_graph(
    signal,
    evidence,
    decision,
    authority,
    time,
    willingness,
    chart_key="governability_graph",
):
    nodes = {
        "Signal": signal,
        "Evidence": evidence,
        "Decision": decision,
        "Authority": authority,
        "Time": time,
        "Willingness": willingness,
    }

    labels = list(nodes.keys())
    values = list(nodes.values())

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=labels,
            y=values,
            mode="lines+markers+text",
            text=labels,
            textposition="top center",
            name="Governability Surface"
        )
    )

    fig.update_layout(
        title="Governability Surface Graph",
        xaxis_title="Correction Surface",
        yaxis_title="Surface Strength",
        yaxis=dict(range=[0, 5]),
        height=450
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key=chart_key
    )