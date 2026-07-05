import streamlit as st

from components.governability_graph import (
    render_governability_graph,
)
from components.influence_network_panel import (
    render_influence_network_panel,
)
from components.network_graph_panel import (
    render_network_graph_panel,
)


def run_visualization_pipeline(
    before_values,
    after_values,
    after_scores,
    weighted_dependency_graph,
):
    st.markdown("---")
    st.header("Governability Graph")

    st.subheader("Before")

    render_governability_graph(
        before_values["signal"],
        before_values["evidence"],
        before_values["decision"],
        before_values["authority"],
        before_values["time"],
        before_values["willingness"],
        chart_key="before_graph",
    )

    st.subheader("After")

    render_governability_graph(
        after_values["signal"],
        after_values["evidence"],
        after_values["decision"],
        after_values["authority"],
        after_values["time"],
        after_values["willingness"],
        chart_key="after_graph",
    )

    render_influence_network_panel(
        after_scores,
        weighted_dependency_graph,
    )

    render_network_graph_panel(
        after_scores,
        weighted_dependency_graph,
    )