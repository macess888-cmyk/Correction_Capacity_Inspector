import json
from pathlib import Path

SNAPSHOT_DIR = Path("snapshots")
SNAPSHOT_DIR.mkdir(exist_ok=True)


def list_snapshots():
    return sorted(
        [f.name for f in SNAPSHOT_DIR.glob("*.json")],
        reverse=True
    )


def load_snapshot(filename):
    filepath = SNAPSHOT_DIR / filename

    with open(filepath, "r") as f:
        return json.load(f)


def save_snapshot(filename, snapshot):
    filepath = SNAPSHOT_DIR / filename

    with open(filepath, "w") as f:
        json.dump(snapshot, f, indent=4)

    return filepath