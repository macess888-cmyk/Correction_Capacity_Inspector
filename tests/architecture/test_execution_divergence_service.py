from models.execution_difference_type import ExecutionDifferenceType
from models.execution_divergence_status import ExecutionDivergenceStatus
from services.execution_divergence_service import ExecutionDivergenceService


def test_identical_states_produce_identical_divergence():

    service = ExecutionDivergenceService()

    divergence = service.inspect(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
    )

    assert divergence.execution_id == "exec-001"
    assert divergence.status == ExecutionDivergenceStatus.IDENTICAL
    assert divergence.differences == ()


def test_different_states_produce_value_difference():

    service = ExecutionDivergenceService()

    divergence = service.inspect(
        execution_id="exec-002",
        runtime_state="RUNNING",
        reconstructed_state="STOPPED",
    )

    assert divergence.status == ExecutionDivergenceStatus.DIVERGED
    assert len(divergence.differences) == 1

    difference = divergence.differences[0]

    assert difference.field_name == "state"
    assert difference.runtime_value == "RUNNING"
    assert difference.reconstructed_value == "STOPPED"
    assert (
        difference.difference_type
        == ExecutionDifferenceType.VALUE_DIFFERENCE
    )


def test_missing_runtime_state_produces_partial_divergence():

    service = ExecutionDivergenceService()

    divergence = service.inspect(
        execution_id="exec-003",
        runtime_state=None,
        reconstructed_state="COMPLETED",
    )

    assert divergence.status == ExecutionDivergenceStatus.PARTIAL
    assert len(divergence.differences) == 1

    difference = divergence.differences[0]

    assert difference.field_name == "state"
    assert difference.runtime_value is None
    assert difference.reconstructed_value == "COMPLETED"
    assert (
        difference.difference_type
        == ExecutionDifferenceType.MISSING_RUNTIME
    )


def test_missing_reconstruction_produces_insufficient_evidence():

    service = ExecutionDivergenceService()

    divergence = service.inspect(
        execution_id="exec-004",
        runtime_state="RUNNING",
        reconstructed_state=None,
    )

    assert (
        divergence.status
        == ExecutionDivergenceStatus.INSUFFICIENT_EVIDENCE
    )
    assert len(divergence.differences) == 1

    difference = divergence.differences[0]

    assert difference.field_name == "state"
    assert difference.runtime_value == "RUNNING"
    assert difference.reconstructed_value is None
    assert (
        difference.difference_type
        == ExecutionDifferenceType.MISSING_RECONSTRUCTION
    )


def test_missing_runtime_and_reconstruction_produces_unknown():

    service = ExecutionDivergenceService()

    divergence = service.inspect(
        execution_id="exec-005",
        runtime_state=None,
        reconstructed_state=None,
    )

    assert divergence.status == ExecutionDivergenceStatus.UNKNOWN
    assert divergence.differences == ()