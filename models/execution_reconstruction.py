from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from models.execution_evidence_completeness import (
    ExecutionEvidenceCompleteness,
)
from models.execution_reconstruction_integrity import (
    ExecutionReconstructionIntegrity,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


@dataclass(frozen=True, slots=True)
class ExecutionReconstruction:
    """
    Evidence-derived reconstruction of one execution.

    This model represents reconstructed historical knowledge
    computed from immutable evidence.

    It is descriptive only.

    It does not execute transitions, authorize action,
    mutate runtime state, or establish historical truth.
    """

    execution_id: str
    grammar_version: str

    reconstructed_status: InspectionExecutionStatus
    reconstructed_stage: str

    operations_applied: tuple[str, ...] = ()
    evidence_processed: int = 0

    integrity: ExecutionReconstructionIntegrity = (
        ExecutionReconstructionIntegrity.UNKNOWN
    )

    completeness: ExecutionEvidenceCompleteness = (
        ExecutionEvidenceCompleteness.UNKNOWN
    )

    warnings: tuple[str, ...] = ()

    constructed_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )