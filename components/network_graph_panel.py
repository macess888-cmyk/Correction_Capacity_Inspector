import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

from engines.network_layout import build_visual_graph


def render_network_graph_panel(
    scores,
    dependency_graph,
):
    st.markdown("---")
    st.header("Visual Influence Network")

    graph_data = build_visual_graph(
        scores,
        dependency_graph,
    )

    graph = nx.DiGraph()

    for node in graph_data["nodes"]:
        graph.add_node(
            node["id"],
            score=node["score"],
            status=node["status"],
            size=node["size"],
        )

    for edge in graph_data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["target"],
            weight=edge["weight"],
            width=edge["width"],
        )

    positions = nx.spring_layout(
        graph,
        seed=42,
    )

    node_sizes = [
        graph.nodes[node]["size"]
        for node in graph.nodes()
    ]

    edge_widths = [
        graph.edges[edge]["width"]
        for edge in graph.edges()
    ]

    labels = {
        node: node
        for node in graph.nodes()
    }

    edge_labels = {
        (source, target): f"{data['weight']:.2f}"
        for source, target, data in graph.edges(data=True)
    }

    fig, ax = plt.subplots(figsize=(10, 7))

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=node_sizes,
        ax=ax,
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        width=edge_widths,
        arrows=True,
        arrowsize=20,
        ax=ax,
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        font_size=9,
        ax=ax,
    )

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=8,
        ax=ax,
    )

    ax.set_axis_off()

    st.pyplot(fig)

    selected_surface = st.selectbox(
        "Inspect Network Surface",
        list(scores.keys()),
        key="network_graph_surface_select",
    )

    incoming = {}
    outgoing = dependency_graph.get(selected_surface, {})

    for source, targets in dependency_graph.items():
        if selected_surface in targets:
            incoming[source] = targets[selected_surface]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Score",
        f"{scores[selected_surface]} / 5",
    )

    c2.metric(
        "Incoming",
        len(incoming),
    )

    c3.metric(
        "Outgoing",
        len(outgoing),
    )

    st.markdown("#### Incoming Influence")

    if incoming:
        for source, weight in incoming.items():
            st.write(
                f"{source} → **{selected_surface}** "
                f"(weight {weight:.2f})"
            )
    else:
        st.info("No incoming influence.")

    st.markdown("#### Outgoing Influence")

    if outgoing:
        for target, weight in outgoing.items():
            st.write(
                f"**{selected_surface}** → {target} "
                f"(weight {weight:.2f})"
            )
    else:
        st.info("No outgoing influence.")