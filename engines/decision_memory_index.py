from engines.decision_history import load_decision_history


def build_memory_index():
    history = load_decision_history()

    index = []

    for item in history:
        index.append(
            {
                "file": item.get("File", ""),
                "strategy": item.get(
                    "Recommended Strategy",
                    "Unknown",
                ),
                "gain": item.get("Projected Gain", 0),
                "uncertainty": item.get(
                    "Uncertainty",
                    "Unknown",
                ),
                "intervention": item.get(
                    "Primary Intervention",
                    "Unknown",
                ),
                "search_text": " ".join(
                    [
                        item.get("File", ""),
                        item.get("Recommended Strategy", ""),
                        item.get("Uncertainty", ""),
                        item.get("Primary Intervention", ""),
                    ]
                ).lower(),
            }
        )

    return index


def search_memory_index(query):
    index = build_memory_index()

    if not query:
        return index

    query = query.lower()

    return [
        item
        for item in index
        if query in item["search_text"]
    ]