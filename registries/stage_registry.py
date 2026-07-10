from typing import List, Optional

from contracts import ReadRegistryContract
from models import Stage


def _build_default_stages() -> List[Stage]:
    return [
        Stage(
            id="stage_reality",
            name="Reality",
            description=(
                "The underlying condition or event before "
                "signal formation."
            ),
            status="Candidate",
            outputs=["Signals"],
            inspection_questions=[
                "What is being treated as real?",
                "What remains unobserved?",
                "What assumptions enter before signal formation?",
            ],
        ),
        Stage(
            id="stage_signals",
            name="Signals",
            description=(
                "Observable traces, indicators, or disturbances "
                "emerging from reality."
            ),
            status="Candidate",
            inputs=["Reality"],
            outputs=["Localization"],
            dependencies=["Reality"],
            inspection_questions=[
                "Are signals visible?",
                "Are signals distorted?",
                "Are signals reproducible?",
            ],
        ),
    ]


class StageRegistry(ReadRegistryContract):
    """
    Provides read-only access to the candidate stage catalog.

    The registry does not mutate stage definitions.
    """

    def __init__(self) -> None:
        self._stages: List[Stage] = _build_default_stages()

    def get_all(self) -> List[Stage]:
        return list(self._stages)

    def get_by_id(
        self,
        stage_id: str,
    ) -> Optional[Stage]:
        for stage in self._stages:
            if stage.id == stage_id:
                return stage

        return None

    def get_by_name(
        self,
        name: str,
    ) -> Optional[Stage]:
        for stage in self._stages:
            if stage.name == name:
                return stage

        return None


def get_stage_registry() -> List[Stage]:
    """
    Compatibility helper preserving the earlier public API.
    """

    return StageRegistry().get_all()


def get_all_stages() -> List[Stage]:
    """
    Compatibility helper preserving the earlier public API.
    """

    return StageRegistry().get_all()


def get_stage_by_name(
    name: str,
) -> Optional[Stage]:
    """
    Compatibility helper preserving the earlier public API.
    """

    return StageRegistry().get_by_name(name)