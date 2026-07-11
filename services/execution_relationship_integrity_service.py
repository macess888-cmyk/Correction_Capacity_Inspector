from models.execution_envelope import ExecutionEnvelope
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)


class ExecutionRelationshipIntegrityService:
    """
    Inspects whether execution governance objects remain valid together.

    Relationship inspection is observational only.
    It grants no authority and performs no execution.
    """

    def inspect(
        self,
        envelope: ExecutionEnvelope,
    ) -> ExecutionRelationshipIntegrity:

        readiness = envelope.readiness
        authorization = readiness.authorization
        plan = authorization.plan
        recommendation = plan.recommendation

        if envelope.execution_id != readiness.execution_id:
            return ExecutionRelationshipIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionRelationshipIntegrityStatus.BROKEN,
                observations=(
                    "Envelope execution identity does not match readiness.",
                ),
            )

        if readiness.execution_id != authorization.execution_id:
            return ExecutionRelationshipIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionRelationshipIntegrityStatus.BROKEN,
                observations=(
                    "Readiness execution identity does not match authorization.",
                ),
            )

        if authorization.execution_id != plan.execution_id:
            return ExecutionRelationshipIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionRelationshipIntegrityStatus.BROKEN,
                observations=(
                    "Authorization execution identity does not match plan.",
                ),
            )

        if plan.execution_id != recommendation.execution_id:
            return ExecutionRelationshipIntegrity(
                execution_id=envelope.execution_id,
                envelope=envelope,
                status=ExecutionRelationshipIntegrityStatus.BROKEN,
                observations=(
                    "Plan execution identity does not match recommendation.",
                ),
            )

        return ExecutionRelationshipIntegrity(
            execution_id=envelope.execution_id,
            envelope=envelope,
            status=ExecutionRelationshipIntegrityStatus.VALID,
            observations=(),
        )