import streamlit as st
import pandas as pd

from engines.influence_network import (
    build_influence_network,
    describe_node,
)


def render_influence_network_panel(
    scores,
    dependency_graph,
):
    st.markdown("---")
    st.header("Interactive Influence Network")

    network = build_influence_network(
        scores,
        dependency_graph,
    )

    st.markdown("### Network Edges")

    edge_rows = []

    for edge in network["edges"]:

        edge_rows.append(
            {
                "From": edge["from"],
                "To": edge["to"],
                "Weight": round(edge["weight"], 2),
                "Visual Width": round(edge["width"], 2),
            }
        )

    st.dataframe(
        pd.DataFrame(edge_rows),
        hide_index=True,
        width="stretch",
    )

    st.markdown("### Surface Inspector")

    selected_surface = st.selectbox(
        "Select Surface",
        list(scores.keys()),
        key="influence_surface_select",
    )

    details = describe_node(
        selected_surface,
        scores,
        dependency_graph,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current Score",
        f"{details['score']} / 5",
    )

    c2.metric(
        "Incoming Links",
        len(details["incoming"]),
    )

    c3.metric(
        "Outgoing Links",
        len(details["outgoing"]),
    )

    st.markdown("#### Incoming Influence")

    if details["incoming"]:

        for source, weight in details["incoming"].items():

            st.write(
                f"**{source}** → {selected_surface} "
                f"(weight {weight:.2f})"
            )

    else:

        st.info("No incoming influence.")

    st.markdown("#### Outgoing Influence")

    if details["outgoing"]:

        for target, weight in details["outgoing"].items():

            st.write(
                f"{selected_surface} → **{target}** "
                f"(weight {weight:.2f})"
            )

    else:

        st.info("No outgoing influence.")

    st.markdown("#### Raw Network Data")

    with st.expander("Show network JSON"):

        st.json(network)