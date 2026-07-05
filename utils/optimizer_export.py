import json
from pathlib import Path
from datetime import datetime


EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def save_optimization_plan(
    budget,
    best_option,
    all_options,
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = EXPORT_DIR / f"optimization_{timestamp}.json"

    data = {
        "timestamp": timestamp,
        "budget": budget,
        "best_intervention": best_option,
        "ranked_options": all_options,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
        )

    return filename