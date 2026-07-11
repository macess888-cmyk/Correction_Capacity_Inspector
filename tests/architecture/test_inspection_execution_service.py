from datetime import UTC

import pytest

from models.inspection_execution import InspectionExecution
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.execution_consistency_record_registry import (
    ExecutionConsistencyRecordRegistry,
)
from registries.execution_transition_definition_registry import (
    ExecutionTransitionDefinitionRegistry,
)
from registries.execution_transition_intent_registry import (
    ExecutionTransitionIntentRegistry,
)
from registries.execution_transition_receipt_registry import (
    ExecutionTransitionReceiptRegistry,
)
from registries.inspection_execution_event_registry import (
    InspectionExecutionEventRegistry,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.execution_consistency_service import (
    ExecutionConsistencyService,
)
from services.execution_transition_coordinator import (
    ExecutionTransitionCoordinator,
)
from services.execution_transition_factory import (
    ExecutionTransitionFactory,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)
from services.inspection_execution_service import (
    InspectionExecutionService,
)


def make_service() -> InspectionExecutionService:
    execution_registry = InspectionExecutionRegistry()

    event_service = InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )

    consistency_service = ExecutionConsistencyService(
        intent_registry=ExecutionTransitionIntentRegistry(),
        receipt_registry=ExecutionTransitionReceiptRegistry(),
        consistency_registry=ExecutionConsistencyRecordRegistry(),
    )

    transition_factory = ExecutionTransitionFactory(
        ExecutionTransitionDefinitionRegistry()
    )

    transition_coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    return InspectionExecutionService(
        registry=execution_registry,
        event_service=event_service,
        transition_factory=transition_factory,
        transition_coordinator=transition_coordinator,
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


def test_service_runs_complete_lifecycle() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    initialized = service.initialize_execution(
        execution_id="execution-001",
        transition_id="transition-initialized-001",
        event_id="event-initialized-001",
        receipt_id="receipt-initialized-001",
        consistency_record_id="record-initialized-001",
    )

    assert initialized.status == (
        InspectionExecutionStatus.INITIALIZED
    )

    running = service.start_execution(
        execution_id="execution-001",
        transition_id="transition-started-001",
        event_id="event-started-001",
        receipt_id="receipt-started-001",
        consistency_record_id="record-started-001",
    )

    assert running.status == InspectionExecutionStatus.RUNNING

    paused = service.pause_execution(
        execution_id="execution-001",
        transition_id="transition-paused-001",
        event_id="event-paused-001",
        receipt_id="receipt-paused-001",
        consistency_record_id="record-paused-001",
    )

    assert paused.status == InspectionExecutionStatus.PAUSED

    resumed = service.resume_execution(
        execution_id="execution-001",
        transition_id="transition-resumed-001",
        event_id="event-resumed-001",
        receipt_id="receipt-resumed-001",
        consistency_record_id="record-resumed-001",
    )

    assert resumed.status == InspectionExecutionStatus.RUNNING

    completed = service.complete_execution(
        execution_id="execution-001",
        transition_id="transition-completed-001",
        event_id="event-completed-001",
        receipt_id="receipt-completed-001",
        consistency_record_id="record-completed-001",
    )

    assert completed.status == (
        InspectionExecutionStatus.COMPLETED
    )
    assert completed.completed is not None
    assert completed.completed.tzinfo == UTC

    archived = service.archive_execution(
        execution_id="execution-001",
        transition_id="transition-archived-001",
        event_id="event-archived-001",
        receipt_id="receipt-archived-001",
        consistency_record_id="record-archived-001",
    )

    assert archived.status == (
        InspectionExecutionStatus.ARCHIVED
    )

    assert [
        event.event_type
        for event in service.list_events_for_execution(
            "execution-001"
        )
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
        execution_id="execution-001",
        transition_id="transition-initialized-001",
        event_id="event-initialized-001",
        receipt_id="receipt-initialized-001",
        consistency_record_id="record-initialized-001",
    )

    service.start_execution(
        execution_id="execution-001",
        transition_id="transition-started-001",
        event_id="event-started-001",
        receipt_id="receipt-started-001",
        consistency_record_id="record-started-001",
    )

    failed = service.fail_execution(
        execution_id="execution-001",
        transition_id="transition-failed-001",
        event_id="event-failed-001",
        receipt_id="receipt-failed-001",
        consistency_record_id="record-failed-001",
        failure_reason="Report creation failed.",
    )

    assert failed.status == InspectionExecutionStatus.FAILED
    assert failed.failure_reason == "Report creation failed."
    assert failed.completed is not None

    failure_event = service.list_events_for_execution(
        "execution-001"
    )[-1]

    assert failure_event.event_type == (
        InspectionExecutionEventType.EXECUTION_FAILED
    )
    assert failure_event.metadata["failure_reason"] == (
        "Report creation failed."
    )


def test_service_cancels_created_execution() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    cancelled = service.cancel_execution(
        execution_id="execution-001",
        transition_id="transition-cancelled-001",
        event_id="event-cancelled-001",
        receipt_id="receipt-cancelled-001",
        consistency_record_id="record-cancelled-001",
    )

    assert cancelled.status == (
        InspectionExecutionStatus.CANCELLED
    )
    assert cancelled.completed is not None


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
            execution_id="execution-001",
            transition_id="transition-completed-001",
            event_id="event-completed-001",
            receipt_id="receipt-completed-001",
            consistency_record_id="record-completed-001",
        )


def test_service_rejects_transition_from_archived() -> None:
    service = make_service()
    execution = make_execution()

    service.create_execution(
        execution,
        event_id="event-created-001",
    )

    service.cancel_execution(
        execution_id="execution-001",
        transition_id="transition-cancelled-001",
        event_id="event-cancelled-001",
        receipt_id="receipt-cancelled-001",
        consistency_record_id="record-cancelled-001",
    )

    service.archive_execution(
        execution_id="execution-001",
        transition_id="transition-archived-001",
        event_id="event-archived-001",
        receipt_id="receipt-archived-001",
        consistency_record_id="record-archived-001",
    )

    with pytest.raises(ValueError):
        service.start_execution(
            execution_id="execution-001",
            transition_id="transition-started-001",
            event_id="event-started-001",
            receipt_id="receipt-started-001",
            consistency_record_id="record-started-001",
        )


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