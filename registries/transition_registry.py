from models import Transition


def get_transition_registry():
    return [
        Transition(
            id="transition_reality_to_signals",
            name="Signal Formation",
            description="Observable signals emerge from reality.",
            status="Candidate",
            source="Reality",
            destination="Signals",
            assumptions=[
                "Reality can produce observable traces.",
                "Signals may be incomplete or distorted.",
            ],
            break_surfaces=[
                "Signal Loss",
            ],
            survivor_conditions=[
                "Historical trace remains available.",
                "Observation can be repeated or reconstructed.",
            ],
            inspection_questions=[
                "Can the signal still be observed?",
                "Has signal distortion occurred?",
                "Is the signal reproducible?",
            ],
        ),
        Transition(
            id="transition_signals_to_localization",
            name="Localization",
            description="Signals are located within a candidate context or system boundary.",
            status="Candidate",
            source="Signals",
            destination="Localization",
            assumptions=[
                "Signals can be associated with a location or boundary.",
                "Localization may be uncertain.",
            ],
            break_surfaces=[
                "Context Loss",
            ],
            survivor_conditions=[
                "Partial signal context remains available.",
            ],
            inspection_questions=[
                "Can the signal source be localized?",
                "What boundaries are being assumed?",
                "What context may be missing?",
            ],
        ),
    ]


def get_all_transitions():
    return get_transition_registry()


def get_transition_by_name(name):
    for transition in get_transition_registry():
        if transition.name == name:
            return transition
    return None


def get_transitions_from_stage(stage_name):
    return [
        transition
        for transition in get_transition_registry()
        if transition.source == stage_name
    ]


def get_transitions_to_stage(stage_name):
    return [
        transition
        for transition in get_transition_registry()
        if transition.destination == stage_name
    ]