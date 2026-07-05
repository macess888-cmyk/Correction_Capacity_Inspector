import json
import os


def load_decision_history(
    output_dir="exports",
):
    if not os.path.exists(output_dir):
        return []

    history = []

    for filename in os.listdir(output_dir):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(output_dir, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                package = json.load(file)

            dashboard = package.get("dashboard", {})
            rationale = package.get("rationale", {})

            history.append(
                {
                    "File": filename,
                    "Exported At": package.get("exported_at", ""),
                    "Recommended Strategy": dashboard.get(
                        "recommended_strategy",
                        rationale.get("recommendation", "Unknown"),
                    ),
                    "Projected Gain": dashboard.get(
                        "projected_gain",
                        0,
                    ),
                    "Monte Carlo Avg": dashboard.get(
                        "monte_carlo_average",
                        0,
                    ),
                    "Uncertainty": dashboard.get(
                        "uncertainty",
                        "Unknown",
                    ),
                    "Primary Intervention": dashboard.get(
                        "primary_intervention",
                        "Unknown",
                    ),
                }
            )

        except Exception as error:
            history.append(
                {
                    "File": filename,
                    "Exported At": "",
                    "Recommended Strategy": "Unreadable package",
                    "Projected Gain": 0,
                    "Monte Carlo Avg": 0,
                    "Uncertainty": str(error),
                    "Primary Intervention": "Unknown",
                }
            )

    history.sort(
        key=lambda item: item["Exported At"],
        reverse=True,
    )

    return history