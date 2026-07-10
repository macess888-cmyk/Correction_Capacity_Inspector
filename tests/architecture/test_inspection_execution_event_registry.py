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


def test_registry_add_get_exists_and_count() -> None:
    registry = InspectionExecutionEventRegistry()
    event = make_event()

    registry.add(event)

    assert registry.get("event-001") is event
    assert registry.exists("event-001") is True
    assert registry.count() == 1


def test_registry_preserves_append_order() -> None:
    registry = InspectionExecutionEventRegistry()

    first = make_event("event-001")
    second = make_event("event-002")

    registry.add(first)
    registry.add(second)

    assert registry.list() == [first, second]


def test_registry_lists_events_for_one_execution() -> None:
    registry = InspectionExecutionEventRegistry()

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

    registry.add(first)
    registry.add(second)
    registry.add(third)

    assert registry.list_for_execution(
        "execution-001"
    ) == [first, third]


def test_registry_counts_events_for_one_execution() -> None:
    registry = InspectionExecutionEventRegistry()

    registry.add(
        make_event(
            event_id="event-001",
            execution_id="execution-001",
        )
    )
    registry.add(
        make_event(
            event_id="event-002",
            execution_id="execution-001",
        )
    )
    registry.add(
        make_event(
            event_id="event-003",
            execution_id="execution-002",
        )
    )

    assert registry.count_for_execution(
        "execution-001"
    ) == 2
    assert registry.count_for_execution(
        "execution-002"
    ) == 1
    assert registry.count_for_execution(
        "missing"
    ) == 0


def test_registry_rejects_duplicate_event_identifier() -> None:
    registry = InspectionExecutionEventRegistry()

    registry.add(make_event("event-001"))

    with pytest.raises(ValueError):
        registry.add(make_event("event-001"))


def test_registry_missing_get_raises_key_error() -> None:
    registry = InspectionExecutionEventRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_has_no_update_operation() -> None:
    registry = InspectionExecutionEventRegistry()

    assert not hasattr(registry, "update")


def test_registry_has_no_remove_operation() -> None:
    registry = InspectionExecutionEventRegistry()

    assert not hasattr(registry, "remove")