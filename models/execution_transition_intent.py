from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


@dataclass(frozen=True, slots=True)
class ExecutionTransitionIntent:
    """
    Immutable declaration of one requested execution transition.

    An intent records what the runtime has been asked to attempt.

    Intent does not prove that state mutation occurred,
    that an event was recorded, or that consistency was achieved.
    """

    transition_id: str
    execution_id: str
    event_id: str

    previous_status: InspectionExecutionStatus
    target_status: InspectionExecutionStatus

    event_type: InspectionExecutionEventType

    target_stage: str
    message: str = ""

    requested_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )