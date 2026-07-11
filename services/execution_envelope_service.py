from datetime import datetime, timezone

from models.execution_envelope import ExecutionEnvelope
from models.execution_envelope_status import ExecutionEnvelopeStatus
from models.execution_readiness import ExecutionReadiness
from models.execution_readiness_status import (
    ExecutionReadinessStatus,
)


class ExecutionEnvelopeService:
    """
    Packages execution readiness into an immutable execution envelope.

    Envelopes preserve governance outputs.
    They grant no authority and perform no execution.
    """

    def create(
        self,
        readiness: ExecutionReadiness,
    ) -> ExecutionEnvelope:

        if readiness.status == ExecutionReadinessStatus.READY:
            status = ExecutionEnvelopeStatus.COMPLETE

        elif readiness.status == ExecutionReadinessStatus.NOT_READY:
            status = ExecutionEnvelopeStatus.INCOMPLETE

        elif readiness.status == ExecutionReadinessStatus.BLOCKED:
            status = ExecutionEnvelopeStatus.INVALID

        else:
            status = ExecutionEnvelopeStatus.UNKNOWN

        return ExecutionEnvelope(
            execution_id=readiness.execution_id,
            readiness=readiness,
            status=status,
            created_at=datetime.now(timezone.utc),
            expires_at=None,
        )