from __future__ import annotations

from dataclasses import dataclass, field

from models.execution_divergence import ExecutionDivergence
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)


@dataclass(frozen=True)
class ExecutionInspection:
    """
    Interprets an execution divergence.

    Inspection is descriptive only.

    It never performs correction.
    """

    execution_id: str

    divergence: ExecutionDivergence

    status: ExecutionInspectionStatus

    observations: tuple[str, ...] = field(default_factory=tuple)

    requires_attention: bool = False