from datetime import datetime

from models.execution_envelope import ExecutionEnvelope
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)


class ExecutionTemporalIntegrityService:
    """
    Inspects whether an execution envelope remains temporally admissible.

    Temporal inspection is observational only.
    It grants no authority and performs no execution.
    """

    def inspect(
        self,
        envelope: ExecutionEnvelope,
        inspected_at: datetime,
    ) -> ExecutionTemporalIntegrity:

        if inspected_at < envelope.created_at:
            return ExecutionTemporalIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionTemporalIntegrityStatus.UNKNOWN,
                inspected_at=inspected_at,
                observations=(
                    "Execution envelope was inspected before "
                    "its creation time.",
                ),
            )

        if (
            envelope.expires_at is not None
            and inspected_at > envelope.expires_at
        ):
            return ExecutionTemporalIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionTemporalIntegrityStatus.EXPIRED,
                inspected_at=inspected_at,
                observations=(
                    "Execution envelope has expired.",
                ),
            )

        return ExecutionTemporalIntegrity(
            execution_id=envelope.execution_id,
            envelope=envelope,
            status=ExecutionTemporalIntegrityStatus.CURRENT,
            inspected_at=inspected_at,
            observations=(),
        )