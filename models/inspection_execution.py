from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


@dataclass(slots=True)
class InspectionExecution:
    """
    Represents one execution attempt for an inspection context.

    This model records runtime state only.

    It does not establish truth, authorize action,
    or make inspection decisions.
    """

    execution_id: str
    inspection_id: str

    status: InspectionExecutionStatus = (
        InspectionExecutionStatus.CREATED
    )

    current_stage: str = "NOT_STARTED"

    attempt: int = 1

    started: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    completed: datetime | None = None

    failure_reason: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)