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
class InspectionExecutionEvent:
    """
    Immutable record of one verified execution lifecycle event.

    The event records runtime behavior only.

    It does not authorize action, establish truth,
    or replace the current execution state.
    """

    event_id: str
    execution_id: str

    event_type: InspectionExecutionEventType

    previous_status: InspectionExecutionStatus
    current_status: InspectionExecutionStatus

    stage: str
    message: str = ""

    recorded_at: datetime = field(
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