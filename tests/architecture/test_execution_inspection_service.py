from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)
from services.execution_inspection_service import (
    ExecutionInspectionService,
)


def test_identical_divergence_is_consistent():

    service = ExecutionInspectionService()

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    inspection = service.inspect(divergence)

    assert inspection.execution_id == "exec-001"
    assert inspection.status == ExecutionInspectionStatus.CONSISTENT
    assert inspection.requires_attention is False
    assert inspection.observations == ()


def test_diverged_execution_is_inconsistent():

    service = ExecutionInspectionService()

    divergence = ExecutionDivergence(
        execution_id="exec-002",
        runtime_state="RUNNING",
        reconstructed_state="STOPPED",
        status=ExecutionDivergenceStatus.DIVERGED,
    )

    inspection = service.inspect(divergence)

    assert inspection.status == ExecutionInspectionStatus.INCONSISTENT
    assert inspection.requires_attention is True
    assert inspection.observations == (
        "Runtime state differs from reconstructed execution state.",
    )


def test_partial_divergence_produces_partial_inspection():

    service = ExecutionInspectionService()

    divergence = ExecutionDivergence(
        execution_id="exec-003",
        runtime_state=None,
        reconstructed_state="COMPLETED",
        status=ExecutionDivergenceStatus.PARTIAL,
    )

    inspection = service.inspect(divergence)

    assert inspection.status == ExecutionInspectionStatus.PARTIAL
    assert inspection.requires_attention is True
    assert inspection.observations == (
        "Runtime execution state is unavailable.",
    )


def test_insufficient_evidence_is_preserved():

    service = ExecutionInspectionService()

    divergence = ExecutionDivergence(
        execution_id="exec-004",
        runtime_state="RUNNING",
        reconstructed_state=None,
        status=ExecutionDivergenceStatus.INSUFFICIENT_EVIDENCE,
    )

    inspection = service.inspect(divergence)

    assert (
        inspection.status
        == ExecutionInspectionStatus.INSUFFICIENT_EVIDENCE
    )
    assert inspection.requires_attention is True
    assert inspection.observations == (
        "Reconstructed execution evidence is insufficient.",
    )


def test_unknown_divergence_produces_unknown_inspection():

    service = ExecutionInspectionService()

    divergence = ExecutionDivergence(
        execution_id="exec-005",
        runtime_state=None,
        reconstructed_state=None,
        status=ExecutionDivergenceStatus.UNKNOWN,
    )

    inspection = service.inspect(divergence)

    assert inspection.status == ExecutionInspectionStatus.UNKNOWN
    assert inspection.requires_attention is True
    assert inspection.observations == (
        "Execution divergence could not be fully interpreted.",
    )