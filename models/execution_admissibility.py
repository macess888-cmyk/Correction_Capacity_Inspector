from __future__ import annotations

from dataclasses import dataclass

from models.execution_context_integrity import (
    ExecutionContextIntegrity,
)
from models.execution_envelope import ExecutionEnvelope
from models.execution_refusal import ExecutionRefusal
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_admissibility_status import (
    ExecutionAdmissibilityStatus,
)


@dataclass(frozen=True)
class ExecutionAdmissibility:
    """
    Represents the constitutional synthesis of execution governance.

    Admissibility determines whether execution may proceed.

    It grants no execution and performs no mutation.
    """

    execution_id: str

    envelope: ExecutionEnvelope

    relationship_integrity: ExecutionRelationshipIntegrity

    temporal_integrity: ExecutionTemporalIntegrity

    context_integrity: ExecutionContextIntegrity

    refusal: ExecutionRefusal

    status: ExecutionAdmissibilityStatus

    reason: str