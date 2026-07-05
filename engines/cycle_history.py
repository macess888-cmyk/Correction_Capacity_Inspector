import json
import os


def load_cycle_history(
    output_dir="exports",
):
    if not os.path.exists(output_dir):
        return []

    rows = []

    for filename in os.listdir(output_dir):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(output_dir, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                package = json.load(file)

            cycle_completion = package.get(
                "cycle_completion",
                {},
            )

            cycle_recommendation = package.get(
                "cycle_recommendation",
                {},
            )

            rows.append(
                {
                    "File": filename,
                    "Exported At": package.get("exported_at", ""),
                    "Completion": cycle_completion.get(
                        "completion_percent",
                        0,
                    ),
                    "Stages Complete": (
                        f"{cycle_completion.get('completed', 0)}"
                        f" / "
                        f"{cycle_completion.get('total', 0)}"
                    ),
                    "Cycle Priority": cycle_recommendation.get(
                        "priority",
                        "Unknown",
                    ),
                    "Cycle Recommendation": cycle_recommendation.get(
                        "recommendation",
                        "Unknown",
                    ),
                }
            )

        except Exception as error:
            rows.append(
                {
                    "File": filename,
                    "Exported At": "",
                    "Completion": 0,
                    "Stages Complete": "0 / 0",
                    "Cycle Priority": "Error",
                    "Cycle Recommendation": str(error),
                }
            )

    rows.sort(
        key=lambda row: row["Exported At"],
        reverse=True,
    )

    return rows