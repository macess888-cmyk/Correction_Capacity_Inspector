from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from models.execution_evidence_completeness import (
    ExecutionEvidenceCompleteness,
)
from models.execution_reconstruction import (
    ExecutionReconstruction,
)
from models.execution_reconstruction_integrity import (
    ExecutionReconstructionIntegrity,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


def make_reconstruction() -> ExecutionReconstruction:
    return ExecutionReconstruction(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        reconstructed_status=(
            InspectionExecutionStatus.COMPLETED
        ),
        reconstructed_stage="COMPLETED",
        operations_applied=(
            "INITIALIZE",
            "START",
            "COMPLETE",
        ),
        evidence_processed=9,
        integrity=(
            ExecutionReconstructionIntegrity.CONSISTENT
        ),
        completeness=(
            ExecutionEvidenceCompleteness.COMPLETE
        ),
        warnings=(
            "No consistency divergence detected.",
        ),
    )


def test_execution_reconstruction_records_derived_values() -> None:
    reconstruction = make_reconstruction()

    assert reconstruction.execution_id == "execution-001"
    assert reconstruction.grammar_version == "v1.4.0"
    assert reconstruction.reconstructed_status == (
        InspectionExecutionStatus.COMPLETED
    )
    assert reconstruction.reconstructed_stage == "COMPLETED"
    assert reconstruction.operations_applied == (
        "INITIALIZE",
        "START",
        "COMPLETE",
    )
    assert reconstruction.evidence_processed == 9

    assert reconstruction.integrity == (
        ExecutionReconstructionIntegrity.CONSISTENT
    )
    assert reconstruction.completeness == (
        ExecutionEvidenceCompleteness.COMPLETE
    )

    assert isinstance(
        reconstruction.integrity,
        ExecutionReconstructionIntegrity,
    )
    assert isinstance(
        reconstruction.completeness,
        ExecutionEvidenceCompleteness,
    )

    assert reconstruction.warnings == (
        "No consistency divergence detected.",
    )


def test_execution_reconstruction_uses_utc_timestamp() -> None:
    reconstruction = make_reconstruction()

    assert isinstance(
        reconstruction.constructed_at,
        datetime,
    )
    assert reconstruction.constructed_at.tzinfo == UTC


def test_execution_reconstruction_is_immutable() -> None:
    reconstruction = make_reconstruction()

    with pytest.raises(FrozenInstanceError):
        reconstruction.reconstructed_stage = (  # type: ignore[misc]
            "CHANGED"
        )


def test_execution_reconstruction_defaults() -> None:
    reconstruction = ExecutionReconstruction(
        execution_id="execution-002",
        grammar_version="v1.4.0",
        reconstructed_status=(
            InspectionExecutionStatus.CREATED
        ),
        reconstructed_stage="NOT_STARTED",
    )

    assert reconstruction.operations_applied == ()
    assert reconstruction.evidence_processed == 0
    assert reconstruction.integrity == (
        ExecutionReconstructionIntegrity.UNKNOWN
    )
    assert reconstruction.completeness == (
        ExecutionEvidenceCompleteness.UNKNOWN
    )
    assert reconstruction.warnings == ()


def test_execution_reconstruction_tuple_fields_are_stable() -> None:
    operations = [
        "INITIALIZE",
        "START",
    ]
    warnings = [
        "Partial evidence.",
    ]

    reconstruction = ExecutionReconstruction(
        execution_id="execution-003",
        grammar_version="v1.4.0",
        reconstructed_status=(
            InspectionExecutionStatus.RUNNING
        ),
        reconstructed_stage="RUNNING",
        operations_applied=tuple(operations),
        warnings=tuple(warnings),
    )

    operations.append("COMPLETE")
    warnings.append("Changed externally.")

    assert reconstruction.operations_applied == (
        "INITIALIZE",
        "START",
    )
    assert reconstruction.warnings == (
        "Partial evidence.",
    )


def test_reconstruction_vocabularies_are_closed() -> None:
    assert {
        integrity.value
        for integrity in ExecutionReconstructionIntegrity
    } == {
        "UNKNOWN",
        "CONSISTENT",
        "INCONSISTENT",
    }

    assert {
        completeness.value
        for completeness in ExecutionEvidenceCompleteness
    } == {
        "UNKNOWN",
        "COMPLETE",
        "PARTIAL",
        "INSUFFICIENT",
    }