from typing import List, Optional

from contracts import ReadRegistryContract
from models import Transition


def _build_default_transitions() -> List[Transition]:
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
            description=(
                "Signals are located within a candidate "
                "context or system boundary."
            ),
            status="Candidate",
            source="Signals",
            destination="Localization",
            assumptions=[
                "Signals can be associated with a location.",
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
                "What boundaries are assumed?",
                "What context may be missing?",
            ],
        ),
    ]


class TransitionRegistry(ReadRegistryContract):
    """
    Read-only registry for candidate transitions.
    """

    def __init__(self) -> None:
        self._transitions = _build_default_transitions()

    def get_all(self) -> List[Transition]:
        return list(self._transitions)

    def get_by_id(
        self,
        transition_id: str,
    ) -> Optional[Transition]:
        for transition in self._transitions:
            if transition.id == transition_id:
                return transition

        return None

    def get_by_name(
        self,
        name: str,
    ) -> Optional[Transition]:
        for transition in self._transitions:
            if transition.name == name:
                return transition

        return None

    def from_stage(
        self,
        stage_name: str,
    ) -> List[Transition]:
        return [
            transition
            for transition in self._transitions
            if transition.source == stage_name
        ]

    def to_stage(
        self,
        stage_name: str,
    ) -> List[Transition]:
        return [
            transition
            for transition in self._transitions
            if transition.destination == stage_name
        ]


def get_transition_registry():
    return TransitionRegistry().get_all()


def get_all_transitions():
    return TransitionRegistry().get_all()


def get_transition_by_name(name):
    return TransitionRegistry().get_by_name(name)


def get_transitions_from_stage(stage_name):
    return TransitionRegistry().from_stage(stage_name)


def get_transitions_to_stage(stage_name):
    return TransitionRegistry().to_stage(stage_name)