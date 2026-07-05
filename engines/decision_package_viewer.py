import json
import os


def list_decision_packages(
    output_dir="exports",
):
    if not os.path.exists(output_dir):
        return []

    return [
        file
        for file in os.listdir(output_dir)
        if file.endswith(".json")
    ]


def load_decision_package(
    filename,
    output_dir="exports",
):
    path = os.path.join(output_dir, filename)

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)