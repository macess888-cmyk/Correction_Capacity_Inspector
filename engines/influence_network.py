def build_influence_network(
    scores,
    dependency_graph,
):
    nodes = []
    edges = []

    for surface, score in scores.items():

        nodes.append(
            {
                "id": surface,
                "label": surface,
                "score": score,
                "size": max(10, score * 8),
            }
        )

    for source, targets in dependency_graph.items():

        for target, weight in targets.items():

            edges.append(
                {
                    "from": source,
                    "to": target,
                    "weight": weight,
                    "width": max(1, weight * 6),
                    "label": f"{weight:.2f}",
                }
            )

    return {
        "nodes": nodes,
        "edges": edges,
    }


def describe_node(
    surface,
    scores,
    dependency_graph,
):
    outgoing = dependency_graph.get(surface, {})

    incoming = {}

    for source, targets in dependency_graph.items():

        if surface in targets:

            incoming[source] = targets[surface]

    return {
        "surface": surface,
        "score": scores.get(surface, 0),
        "incoming": incoming,
        "outgoing": outgoing,
    }