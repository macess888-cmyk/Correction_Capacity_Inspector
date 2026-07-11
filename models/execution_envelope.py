from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from models.execution_envelope_status import ExecutionEnvelopeStatus
from models.execution_readiness import ExecutionReadiness


@dataclass(frozen=True)
class ExecutionEnvelope:
    """
    Represents an immutable package presented to an execution engine.

    The envelope preserves execution readiness and its upstream
    governance chain.

    It grants no authority and performs no execution.
    """

    execution_id: str

    readiness: ExecutionReadiness

    status: ExecutionEnvelopeStatus

    created_at: datetime

    expires_at: datetime | None = None