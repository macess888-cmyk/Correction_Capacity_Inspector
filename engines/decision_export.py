from datetime import datetime
import json
import os


def export_decision_package(
    dashboard,
    rationale,
    scenario_rows,
    cycle=None,
    cycle_completion=None,
    cycle_risks=None,
    cycle_recommendation=None,
    output_dir="exports",
):
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    package = {
        "exported_at": timestamp,
        "dashboard": dashboard,
        "rationale": rationale,
        "scenarios": scenario_rows,
        "cycle": cycle,
        "cycle_completion": cycle_completion,
        "cycle_risks": cycle_risks,
        "cycle_recommendation": cycle_recommendation,
    }

    filename = os.path.join(
        output_dir,
        f"decision_package_{timestamp}.json",
    )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(package, file, indent=2, default=str)

    return filename