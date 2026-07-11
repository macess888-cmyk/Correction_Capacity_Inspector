from models.execution_admissibility import ExecutionAdmissibility
from models.execution_admissibility_status import (
    ExecutionAdmissibilityStatus,
)
from models.execution_context_integrity import (
    ExecutionContextIntegrity,
)
from models.execution_context_integrity_status import (
    ExecutionContextIntegrityStatus,
)
from models.execution_envelope import ExecutionEnvelope
from models.execution_refusal import ExecutionRefusal
from models.execution_refusal_status import (
    ExecutionRefusalStatus,
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


class ExecutionAdmissibilityService:
    """
    Synthesizes execution governance into an admissibility result.

    Admissibility grants no execution and performs no mutation.
    """

    def assess(
        self,
        envelope: ExecutionEnvelope,
        relationship_integrity: ExecutionRelationshipIntegrity,
        temporal_integrity: ExecutionTemporalIntegrity,
        context_integrity: ExecutionContextIntegrity,
        refusal: ExecutionRefusal,
    ) -> ExecutionAdmissibility:

        if refusal.status == ExecutionRefusalStatus.REFUSED:
            status = ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
            reason = "Execution refusal has been established."

        elif refusal.status == ExecutionRefusalStatus.INDETERMINATE:
            status = ExecutionAdmissibilityStatus.INDETERMINATE
            reason = "Execution refusal is indeterminate."

        elif (
            relationship_integrity.status
            != ExecutionRelationshipIntegrityStatus.VALID
        ):
            status = ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
            reason = "Execution relationship integrity is not valid."

        elif (
            temporal_integrity.status
            == ExecutionTemporalIntegrityStatus.UNKNOWN
        ):
            status = ExecutionAdmissibilityStatus.INDETERMINATE
            reason = (
                "Execution temporal integrity could not be established."
            )

        elif (
            temporal_integrity.status
            != ExecutionTemporalIntegrityStatus.CURRENT
        ):
            status = ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
            reason = "Execution temporal integrity is not current."

        elif (
            context_integrity.status
            == ExecutionContextIntegrityStatus.INCOMPLETE
        ):
            status = ExecutionAdmissibilityStatus.INDETERMINATE
            reason = "Execution context integrity is incomplete."

        elif (
            context_integrity.status
            == ExecutionContextIntegrityStatus.UNKNOWN
        ):
            status = ExecutionAdmissibilityStatus.UNKNOWN
            reason = (
                "Execution context integrity could not be established."
            )

        elif (
            context_integrity.status
            != ExecutionContextIntegrityStatus.CORRESPONDING
        ):
            status = ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
            reason = (
                "Execution context integrity is not corresponding."
            )

        else:
            status = ExecutionAdmissibilityStatus.ADMISSIBLE
            reason = "All execution governance conditions are satisfied."

        return ExecutionAdmissibility(
            execution_id=envelope.execution_id,
            envelope=envelope,
            relationship_integrity=relationship_integrity,
            temporal_integrity=temporal_integrity,
            context_integrity=context_integrity,
            refusal=refusal,
            status=status,
            reason=reason,
        )