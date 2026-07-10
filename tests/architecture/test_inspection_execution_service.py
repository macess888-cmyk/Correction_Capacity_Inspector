from datetime import UTC

import pytest

from models.inspection_execution import InspectionExecution
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.inspection_execution_event_registry import (
    InspectionExecutionEventRegistry,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)
from services.inspection_execution_service import (
    InspectionExecutionService,
)


def make_service() -> InspectionExecutionService:
    event_service = InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )

    return InspectionExecutionService(
        registry=InspectionExecutionRegistry(),
        event_service=event_service,
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

    created = service.create_execution(
        execution,
        event_id="event-created-001",
    )

    assert created is execution
    assert service.get_execution("execution-001") is execution
    assert service.execution_exists("execution-001") is True
    assert service.count_executions() == 1

    events = service.list_events_for_execution(
        "execution-001"
    )

    assert len(events) == 1
    assert events[0].event_type == (
        InspectionExecutionEventType.EXECUTION_CREATED
    )
    assert events[0].previous_status == (
        InspectionExecutionStatus.CREATED
    )
    assert events[0].current_status == (
        InspectionExecutionStatus.CREATED
    )


def test_service_runs_complete_lifecycle() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    initialized = service.initialize_execution(
        "execution-001",
        event_id="event-initialized-001",
    )
    assert initialized.status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert initialized.current_stage == "INITIALIZED"

    running = service.start_execution(
        "execution-001",
        event_id="event-started-001",
    )
    assert running.status == InspectionExecutionStatus.RUNNING
    assert running.current_stage == "RUNNING"

    paused = service.pause_execution(
        "execution-001",
        event_id="event-paused-001",
    )
    assert paused.status == InspectionExecutionStatus.PAUSED
    assert paused.current_stage == "PAUSED"

    resumed = service.resume_execution(
        "execution-001",
        event_id="event-resumed-001",
    )
    assert resumed.status == InspectionExecutionStatus.RUNNING

    completed = service.complete_execution(
        "execution-001",
        event_id="event-completed-001",
    )
    assert completed.status == (
        InspectionExecutionStatus.COMPLETED
    )
    assert completed.completed is not None
    assert completed.completed.tzinfo == UTC

    archived = service.archive_execution(
        "execution-001",
        event_id="event-archived-001",
    )
    assert archived.status == (
        InspectionExecutionStatus.ARCHIVED
    )
    assert archived.current_stage == "ARCHIVED"

    events = service.list_events_for_execution(
        "execution-001"
    )

    assert [
        event.event_type
        for event in events
    ] == [
        InspectionExecutionEventType.EXECUTION_CREATED,
        InspectionExecutionEventType.EXECUTION_INITIALIZED,
        InspectionExecutionEventType.EXECUTION_STARTED,
        InspectionExecutionEventType.EXECUTION_PAUSED,
        InspectionExecutionEventType.EXECUTION_RESUMED,
        InspectionExecutionEventType.EXECUTION_COMPLETED,
        InspectionExecutionEventType.EXECUTION_ARCHIVED,
    ]


def test_service_fails_execution_with_reason() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )
    service.initialize_execution(
        "execution-001",
        event_id="event-initialized-001",
    )
    service.start_execution(
        "execution-001",
        event_id="event-started-001",
    )

    failed = service.fail_execution(
        "execution-001",
        event_id="event-failed-001",
        failure_reason="Report creation failed.",
    )

    assert failed.status == InspectionExecutionStatus.FAILED
    assert failed.current_stage == "FAILED"
    assert failed.failure_reason == "Report creation failed."
    assert failed.completed is not None
    assert failed.completed.tzinfo == UTC

    events = service.list_events_for_execution(
        "execution-001"
    )
    failure_event = events[-1]

    assert failure_event.event_type == (
        InspectionExecutionEventType.EXECUTION_FAILED
    )
    assert failure_event.metadata[
        "failure_reason"
    ] == "Report creation failed."


def test_service_cancels_created_execution() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    cancelled = service.cancel_execution(
        "execution-001",
        event_id="event-cancelled-001",
    )

    assert cancelled.status == (
        InspectionExecutionStatus.CANCELLED
    )
    assert cancelled.completed is not None

    events = service.list_events_for_execution(
        "execution-001"
    )

    assert events[-1].event_type == (
        InspectionExecutionEventType.EXECUTION_CANCELLED
    )


def test_service_rejects_invalid_transition() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Invalid inspection execution transition: "
            "CREATED -> COMPLETED"
        ),
    ):
        service.complete_execution(
            "execution-001",
            event_id="event-completed-001",
        )

    assert len(
        service.list_events_for_execution("execution-001")
    ) == 1


def test_service_rejects_transition_from_archived() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )
    service.cancel_execution(
        "execution-001",
        event_id="event-cancelled-001",
    )
    service.archive_execution(
        "execution-001",
        event_id="event-archived-001",
    )

    with pytest.raises(ValueError):
        service.start_execution(
            "execution-001",
            event_id="event-started-001",
        )

    assert len(
        service.list_events_for_execution("execution-001")
    ) == 3


def test_service_lists_executions() -> None:
    service = make_service()

    first = make_execution("execution-001")
    second = make_execution("execution-002")

    service.create_execution(
        first,
        event_id="event-created-001",
    )
    service.create_execution(
        second,
        event_id="event-created-002",
    )

    assert service.list_executions() == [first, second]


def test_duplicate_event_identifier_fails_visibly() -> None:
    service = make_service()

    first = make_execution("execution-001")
    second = make_execution("execution-002")

    service.create_execution(
        first,
        event_id="event-created-shared",
    )

    with pytest.raises(ValueError):
        service.create_execution(
            second,
            event_id="event-created-shared",
        )