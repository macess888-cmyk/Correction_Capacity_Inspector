from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.execution_envelope import ExecutionEnvelope
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)


@dataclass(frozen=True)
class ExecutionTemporalIntegrity:
    """
    Describes whether an execution envelope and its preserved
    governance chain remain temporally admissible.

    This model is observational only.

    It grants no authority and performs no execution.
    """

    execution_id: str

    envelope: ExecutionEnvelope

    status: ExecutionTemporalIntegrityStatus

    inspected_at: datetime

    observations: tuple[str, ...] = field(default_factory=tuple)