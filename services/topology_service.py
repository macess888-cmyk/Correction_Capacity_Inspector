from registries.stage_registry import get_all_stages
from registries.transition_registry import (
    get_transitions_from_stage,
    get_transitions_to_stage,
)


def get_stage_overview(stage_name):
    stage = None

    for candidate in get_all_stages():
        if candidate.name == stage_name:
            stage = candidate
            break

    if stage is None:
        return None

    return {
        "stage": stage,
        "incoming": get_transitions_to_stage(stage_name),
        "outgoing": get_transitions_from_stage(stage_name),
    }


def get_complete_topology():
    return get_all_stages()