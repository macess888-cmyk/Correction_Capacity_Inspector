from __future__ import annotations

from dataclasses import dataclass

from models.execution_envelope import ExecutionEnvelope
from models.execution_refusal_status import ExecutionRefusalStatus
from models.execution_refusal_type import ExecutionRefusalType
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)


@dataclass(frozen=True)
class ExecutionRefusal:
    """
    Represents an immutable decision not to execute.

    Refusal is a governed outcome, not an exception.

    It performs no mutation and no execution.
    """

    execution_id: str

    envelope: ExecutionEnvelope

    relationship_integrity: ExecutionRelationshipIntegrity

    temporal_integrity: ExecutionTemporalIntegrity

    status: ExecutionRefusalStatus

    refusal_type: ExecutionRefusalType

    reason: str