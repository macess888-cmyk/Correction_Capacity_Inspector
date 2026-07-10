import pytest

from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.inspection_execution_event_registry import (
    InspectionExecutionEventRegistry,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)


def make_service() -> InspectionExecutionEventService:
    return InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )


def make_event(
    event_id: str = "event-001",
    execution_id: str = "execution-001",
) -> InspectionExecutionEvent:
    return InspectionExecutionEvent(
        event_id=event_id,
        execution_id=execution_id,
        event_type=(
            InspectionExecutionEventType.EXECUTION_STARTED
        ),
        previous_status=(
            InspectionExecutionStatus.INITIALIZED
        ),
        current_status=(
            InspectionExecutionStatus.RUNNING
        ),
        stage="RUNNING",
        message="Execution started.",
    )


def test_service_records_and_gets_event() -> None:
    service = make_service()
    event = make_event()

    service.record_event(event)

    assert service.get_event("event-001") is event
    assert service.event_exists("event-001") is True


def test_service_lists_events_in_append_order() -> None:
    service = make_service()

    first = make_event("event-001")
    second = make_event("event-002")

    service.record_event(first)
    service.record_event(second)

    assert service.list_events() == [first, second]


def test_service_lists_events_for_execution() -> None:
    service = make_service()

    first = make_event(
        event_id="event-001",
        execution_id="execution-001",
    )
    second = make_event(
        event_id="event-002",
        execution_id="execution-002",
    )
    third = make_event(
        event_id="event-003",
        execution_id="execution-001",
    )

    service.record_event(first)
    service.record_event(second)
    service.record_event(third)

    assert service.list_events_for_execution(
        "execution-001"
    ) == [first, third]


def test_service_counts_events() -> None:
    service = make_service()

    service.record_event(
        make_event(
            event_id="event-001",
            execution_id="execution-001",
        )
    )
    service.record_event(
        make_event(
            event_id="event-002",
            execution_id="execution-001",
        )
    )
    service.record_event(
        make_event(
            event_id="event-003",
            execution_id="execution-002",
        )
    )

    assert service.count_events() == 3
    assert service.count_events_for_execution(
        "execution-001"
    ) == 2
    assert service.count_events_for_execution(
        "execution-002"
    ) == 1
    assert service.count_events_for_execution(
        "missing"
    ) == 0


def test_service_rejects_duplicate_event_identifier() -> None:
    service = make_service()

    service.record_event(make_event("event-001"))

    with pytest.raises(ValueError):
        service.record_event(make_event("event-001"))


def test_service_has_no_update_operation() -> None:
    service = make_service()

    assert not hasattr(service, "update_event")


def test_service_has_no_remove_operation() -> None:
    service = make_service()

    assert not hasattr(service, "remove_event")