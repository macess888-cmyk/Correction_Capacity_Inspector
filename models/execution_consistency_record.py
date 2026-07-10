from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


@dataclass(frozen=True, slots=True)
class ExecutionConsistencyRecord:
    """
    Immutable record of a detected transition consistency issue.

    Compensation does not erase this record.

    The record preserves the attempted transition boundary
    for later inspection and recovery.
    """

    record_id: str
    transition_id: str
    execution_id: str

    consistency_status: ExecutionConsistencyStatus

    expected_status: InspectionExecutionStatus
    observed_status: InspectionExecutionStatus

    expected_event_id: str

    failure_stage: str
    failure_reason: str

    compensation_attempted: bool = False
    compensation_succeeded: bool = False

    detected_at: datetime = field(
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