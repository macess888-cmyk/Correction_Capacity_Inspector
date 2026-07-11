from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from models.execution_context_integrity_status import (
    ExecutionContextIntegrityStatus,
)
from models.execution_envelope import ExecutionEnvelope


@dataclass(frozen=True)
class ExecutionContextIntegrity:
    """
    Describes whether an execution envelope remains valid
    under the currently observed operational context.

    Context inspection is observational only.

    It grants no authority and performs no execution.
    """

    execution_id: str

    envelope: ExecutionEnvelope

    expected_context: Mapping[str, object]

    observed_context: Mapping[str, object]

    status: ExecutionContextIntegrityStatus

    observations: tuple[str, ...] = field(default_factory=tuple)