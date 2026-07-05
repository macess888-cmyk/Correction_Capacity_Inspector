def node_status(score):
    if score >= 4:
        return "strong"
    elif score >= 3:
        return "stable"
    elif score >= 2:
        return "weak"
    else:
        return "critical"


def build_visual_graph(
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
                "status": node_status(score),
                "size": max(300, score * 300),
            }
        )

    for source, targets in dependency_graph.items():
        for target, weight in targets.items():
            edges.append(
                {
                    "source": source,
                    "target": target,
                    "weight": weight,
                    "width": max(1, weight * 4),
                    "label": f"{weight:.2f}",
                }
            )

    return {
        "nodes": nodes,
        "edges": edges,
    }