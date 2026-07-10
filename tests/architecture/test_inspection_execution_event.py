from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

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


def make_event() -> InspectionExecutionEvent:
    return InspectionExecutionEvent(
        event_id="event-001",
        execution_id="execution-001",
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
        metadata={
            "source": "architecture-test",
        },
    )


def test_execution_event_records_typed_values() -> None:
    event = make_event()

    assert event.event_id == "event-001"
    assert event.execution_id == "execution-001"
    assert event.event_type == (
        InspectionExecutionEventType.EXECUTION_STARTED
    )
    assert event.previous_status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert event.current_status == (
        InspectionExecutionStatus.RUNNING
    )
    assert event.stage == "RUNNING"
    assert event.message == "Execution started."


def test_execution_event_uses_timezone_aware_timestamp() -> None:
    event = make_event()

    assert isinstance(event.recorded_at, datetime)
    assert event.recorded_at.tzinfo == UTC


def test_execution_event_fields_are_immutable() -> None:
    event = make_event()

    with pytest.raises(FrozenInstanceError):
        event.stage = "CHANGED"  # type: ignore[misc]


def test_execution_event_metadata_is_immutable() -> None:
    event = make_event()

    with pytest.raises(TypeError):
        event.metadata["source"] = "changed"  # type: ignore[index]


def test_execution_event_copies_input_metadata() -> None:
    source_metadata = {
        "source": "original",
    }

    event = InspectionExecutionEvent(
        event_id="event-002",
        execution_id="execution-001",
        event_type=(
            InspectionExecutionEventType.EXECUTION_PAUSED
        ),
        previous_status=InspectionExecutionStatus.RUNNING,
        current_status=InspectionExecutionStatus.PAUSED,
        stage="PAUSED",
        metadata=source_metadata,
    )

    source_metadata["source"] = "changed"

    assert event.metadata["source"] == "original"


def test_event_type_vocabulary_is_closed() -> None:
    expected = {
        "EXECUTION_CREATED",
        "EXECUTION_INITIALIZED",
        "EXECUTION_STARTED",
        "EXECUTION_PAUSED",
        "EXECUTION_RESUMED",
        "EXECUTION_COMPLETED",
        "EXECUTION_FAILED",
        "EXECUTION_CANCELLED",
        "EXECUTION_ARCHIVED",
    }

    assert {
        event_type.value
        for event_type in InspectionExecutionEventType
    } == expected