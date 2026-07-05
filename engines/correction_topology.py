CORRECTION_TOPOLOGY = [
    "Reality",
    "Signals",
    "Localization",
    "Witness Formation",
    "Interpretation",
    "Accountability",
    "Correction Capacity",
    "Recovery",
    "Governability",
    "Future Influence",
    "Inspectable Unknowns",
]

BREAK_SURFACES = [
    {
        "name": "Signal Loss",
        "between": ("Reality", "Signals"),
        "description": "Reality fails to produce or preserve usable signals.",
    },
    {
        "name": "Witness Loss",
        "between": ("Localization", "Witness Formation"),
        "description": "A localized signal fails to become independently witnessable.",
    },
    {
        "name": "Context Loss",
        "between": ("Witness Formation", "Interpretation"),
        "description": "Witnessed material loses the context needed for interpretation.",
    },
    {
        "name": "Attribution Loss",
        "between": ("Interpretation", "Accountability"),
        "description": "Interpretation fails to support accountable attribution.",
    },
    {
        "name": "Correction Loss",
        "between": ("Accountability", "Correction Capacity"),
        "description": "Accountability no longer preserves actionable correction capacity.",
    },
    {
        "name": "Optionality Loss",
        "between": ("Recovery", "Governability"),
        "description": "Recovery no longer preserves enough future influence.",
    },
]


def get_topology():
    return CORRECTION_TOPOLOGY


def get_break_surfaces():
    return BREAK_SURFACES


def get_forward_path():
    return list(zip(CORRECTION_TOPOLOGY, CORRECTION_TOPOLOGY[1:]))


def get_reverse_path():
    return list(reversed(get_forward_path()))

def previous_stage(stage):

    topology = get_topology()

    if stage not in topology:
        return None

    index = topology.index(stage)

    if index == 0:
        return None

    return topology[index - 1]

def next_stage(stage):

    topology = get_topology()

    if stage not in topology:
        return None

    index = topology.index(stage)

    if index == len(topology) - 1:
        return None

    return topology[index + 1]

def break_surfaces_for_stage(stage):

    surfaces = get_break_surfaces()

    return [
        surface
        for surface in surfaces
        if stage in surface["between"]
    ]