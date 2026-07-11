from __future__ import annotations

from dataclasses import dataclass, field

from models.execution_envelope import ExecutionEnvelope
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)


@dataclass(frozen=True)
class ExecutionRelationshipIntegrity:
    """
    Describes whether the relationships preserved within
    an execution envelope remain valid together.

    This model is observational only.

    It grants no authority and performs no execution.
    """

    execution_id: str

    envelope: ExecutionEnvelope

    status: ExecutionRelationshipIntegrityStatus

    observations: tuple[str, ...] = field(default_factory=tuple)