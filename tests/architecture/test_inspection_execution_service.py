from datetime import UTC

import pytest

from models.inspection_execution import InspectionExecution
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.inspection_execution_service import (
    InspectionExecutionService,
)


def make_service() -> InspectionExecutionService:
    return InspectionExecutionService(
        InspectionExecutionRegistry()
    )


def make_execution(
    execution_id: str = "execution-001",
) -> InspectionExecution:
    return InspectionExecution(
        execution_id=execution_id,
        inspection_id="inspection-001",
    )


def test_service_creates_and_gets_execution() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)

    assert service.get_execution("execution-001") is execution
    assert service.execution_exists("execution-001") is True
    assert service.count_executions() == 1


def test_service_runs_complete_lifecycle() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)

    initialized = service.initialize_execution("execution-001")
    assert initialized.status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert initialized.current_stage == "INITIALIZED"

    running = service.start_execution("execution-001")
    assert running.status == InspectionExecutionStatus.RUNNING
    assert running.current_stage == "RUNNING"

    paused = service.pause_execution("execution-001")
    assert paused.status == InspectionExecutionStatus.PAUSED
    assert paused.current_stage == "PAUSED"

    resumed = service.resume_execution("execution-001")
    assert resumed.status == InspectionExecutionStatus.RUNNING

    completed = service.complete_execution("execution-001")
    assert completed.status == (
        InspectionExecutionStatus.COMPLETED
    )
    assert completed.completed is not None
    assert completed.completed.tzinfo == UTC

    archived = service.archive_execution("execution-001")
    assert archived.status == InspectionExecutionStatus.ARCHIVED
    assert archived.current_stage == "ARCHIVED"


def test_service_fails_execution_with_reason() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)
    service.initialize_execution("execution-001")
    service.start_execution("execution-001")

    failed = service.fail_execution(
        "execution-001",
        "Report creation failed.",
    )

    assert failed.status == InspectionExecutionStatus.FAILED
    assert failed.current_stage == "FAILED"
    assert failed.failure_reason == "Report creation failed."
    assert failed.completed is not None
    assert failed.completed.tzinfo == UTC


def test_service_cancels_created_execution() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)

    cancelled = service.cancel_execution("execution-001")

    assert cancelled.status == (
        InspectionExecutionStatus.CANCELLED
    )
    assert cancelled.completed is not None


def test_service_rejects_invalid_transition() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)

    with pytest.raises(
        ValueError,
        match=(
            "Invalid inspection execution transition: "
            "CREATED -> COMPLETED"
        ),
    ):
        service.complete_execution("execution-001")


def test_service_rejects_transition_from_archived() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(execution)
    service.cancel_execution("execution-001")
    service.archive_execution("execution-001")

    with pytest.raises(ValueError):
        service.start_execution("execution-001")


def test_service_lists_executions() -> None:
    service = make_service()

    first = make_execution("execution-001")
    second = make_execution("execution-002")

    service.create_execution(first)
    service.create_execution(second)

    assert service.list_executions() == [first, second]