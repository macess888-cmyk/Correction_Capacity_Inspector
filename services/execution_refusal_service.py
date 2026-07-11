from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_envelope import ExecutionEnvelope
from models.execution_envelope_status import (
    ExecutionEnvelopeStatus,
)
from models.execution_readiness_status import (
    ExecutionReadinessStatus,
)
from models.execution_refusal import ExecutionRefusal
from models.execution_refusal_status import (
    ExecutionRefusalStatus,
)
from models.execution_refusal_type import (
    ExecutionRefusalType,
)
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)


class ExecutionRefusalService:
    """
    Evaluates whether execution must be refused.

    Refusal is a governed outcome rather than an exception.
    """

    def evaluate(
        self,
        envelope: ExecutionEnvelope,
        relationship_integrity: ExecutionRelationshipIntegrity,
        temporal_integrity: ExecutionTemporalIntegrity,
    ) -> ExecutionRefusal:

        if envelope.status == ExecutionEnvelopeStatus.INVALID:
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.ENVELOPE_INVALID,
                reason="Execution envelope is invalid.",
            )

        if envelope.status == ExecutionEnvelopeStatus.INCOMPLETE:
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.ENVELOPE_INCOMPLETE,
                reason="Execution envelope is incomplete.",
            )

        if (
            relationship_integrity.status
            == ExecutionRelationshipIntegrityStatus.BROKEN
        ):
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.RELATIONSHIP_BROKEN,
                reason="Execution relationship integrity is broken.",
            )

        if (
            temporal_integrity.status
            == ExecutionTemporalIntegrityStatus.EXPIRED
        ):
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.TEMPORALLY_EXPIRED,
                reason="Execution envelope is temporally expired.",
            )

        if (
            temporal_integrity.status
            == ExecutionTemporalIntegrityStatus.UNKNOWN
        ):
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.INDETERMINATE,
                refusal_type=ExecutionRefusalType.TEMPORALLY_UNKNOWN,
                reason="Execution temporal integrity could not be established.",
            )

        if (
            envelope.readiness.status
            == ExecutionReadinessStatus.NOT_READY
        ):
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.NOT_READY,
                reason="Execution is not ready.",
            )

        if (
            envelope.readiness.authorization.status
            == ExecutionAuthorizationStatus.NOT_AUTHORIZED
        ):
            return ExecutionRefusal(
                execution_id=envelope.execution_id,
                envelope=envelope,
                relationship_integrity=relationship_integrity,
                temporal_integrity=temporal_integrity,
                status=ExecutionRefusalStatus.REFUSED,
                refusal_type=ExecutionRefusalType.NOT_AUTHORIZED,
                reason="Execution is not authorized.",
            )

        return ExecutionRefusal(
            execution_id=envelope.execution_id,
            envelope=envelope,
            relationship_integrity=relationship_integrity,
            temporal_integrity=temporal_integrity,
            status=ExecutionRefusalStatus.NOT_REFUSED,
            refusal_type=ExecutionRefusalType.UNKNOWN,
            reason="No refusal condition was established.",
        )