from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)
from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


def make_intent() -> ExecutionTransitionIntent:
    return ExecutionTransitionIntent(
        transition_id="transition-001",
        execution_id="execution-001",
        event_id="event-001",
        previous_status=InspectionExecutionStatus.INITIALIZED,
        target_status=InspectionExecutionStatus.RUNNING,
        event_type=(
            InspectionExecutionEventType.EXECUTION_STARTED
        ),
        target_stage="RUNNING",
        message="Start execution.",
        metadata={
            "source": "architecture-test",
        },
    )


def test_transition_intent_is_typed_and_immutable() -> None:
    intent = make_intent()

    assert intent.previous_status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert intent.target_status == (
        InspectionExecutionStatus.RUNNING
    )
    assert intent.event_type == (
        InspectionExecutionEventType.EXECUTION_STARTED
    )
    assert intent.requested_at.tzinfo == UTC

    with pytest.raises(FrozenInstanceError):
        intent.target_stage = "CHANGED"  # type: ignore[misc]

    with pytest.raises(TypeError):
        intent.metadata["source"] = "changed"  # type: ignore[index]


def test_transition_intent_copies_input_metadata() -> None:
    metadata = {
        "source": "original",
    }

    intent = ExecutionTransitionIntent(
        transition_id="transition-002",
        execution_id="execution-001",
        event_id="event-002",
        previous_status=InspectionExecutionStatus.RUNNING,
        target_status=InspectionExecutionStatus.PAUSED,
        event_type=(
            InspectionExecutionEventType.EXECUTION_PAUSED
        ),
        target_stage="PAUSED",
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert intent.metadata["source"] == "original"


def test_transition_receipt_records_consistent_outcome() -> None:
    receipt = ExecutionTransitionReceipt(
        receipt_id="receipt-001",
        transition_id="transition-001",
        execution_id="execution-001",
        state_updated=True,
        event_recorded=True,
        consistency_status=(
            ExecutionConsistencyStatus.CONSISTENT
        ),
        metadata={
            "source": "architecture-test",
        },
    )

    assert receipt.state_updated is True
    assert receipt.event_recorded is True
    assert receipt.consistency_status == (
        ExecutionConsistencyStatus.CONSISTENT
    )
    assert isinstance(receipt.completed_at, datetime)
    assert receipt.completed_at.tzinfo == UTC

    with pytest.raises(FrozenInstanceError):
        receipt.failure_stage = "changed"  # type: ignore[misc]

    with pytest.raises(TypeError):
        receipt.metadata["source"] = "changed"  # type: ignore[index]


def test_consistency_record_preserves_divergence() -> None:
    record = ExecutionConsistencyRecord(
        record_id="record-001",
        transition_id="transition-001",
        execution_id="execution-001",
        consistency_status=(
            ExecutionConsistencyStatus.RECOVERY_REQUIRED
        ),
        expected_status=InspectionExecutionStatus.RUNNING,
        observed_status=InspectionExecutionStatus.INITIALIZED,
        expected_event_id="event-001",
        failure_stage="EVENT_RECORDING",
        failure_reason="Event persistence failed.",
        compensation_attempted=True,
        compensation_succeeded=False,
        metadata={
            "source": "architecture-test",
        },
    )

    assert record.consistency_status == (
        ExecutionConsistencyStatus.RECOVERY_REQUIRED
    )
    assert record.expected_status == (
        InspectionExecutionStatus.RUNNING
    )
    assert record.observed_status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert record.compensation_attempted is True
    assert record.compensation_succeeded is False
    assert record.detected_at.tzinfo == UTC

    with pytest.raises(FrozenInstanceError):
        record.failure_reason = "changed"  # type: ignore[misc]

    with pytest.raises(TypeError):
        record.metadata["source"] = "changed"  # type: ignore[index]


def test_consistency_status_vocabulary_is_closed() -> None:
    assert {
        status.value
        for status in ExecutionConsistencyStatus
    } == {
        "PENDING",
        "CONSISTENT",
        "STATE_NOT_UPDATED",
        "EVENT_NOT_RECORDED",
        "COMPENSATED",
        "RECOVERY_REQUIRED",
    }