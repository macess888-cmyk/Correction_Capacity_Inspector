from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_audit_event import ExecutionAuditEvent
from models.execution_audit_event_type import ExecutionAuditEventType


def make_audit_event() -> ExecutionAuditEvent:
    return ExecutionAuditEvent(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={
            "action": "reconcile",
        },
        sequence_number=1,
    )


def test_execution_audit_event_can_be_created():
    event = make_audit_event()

    assert event.execution_audit_event_id == "AUDIT-001"
    assert event.execution_intent_id == "INTENT-001"
    assert event.execution_result_id is None
    assert event.event_type is ExecutionAuditEventType.INTENT_RECEIVED
    assert event.details["action"] == "reconcile"
    assert event.sequence_number == 1


def test_execution_audit_event_is_immutable():
    event = make_audit_event()

    with pytest.raises(FrozenInstanceError):
        event.sequence_number = 2


def test_execution_audit_event_details_are_immutable():
    event = make_audit_event()

    with pytest.raises(TypeError):
        event.details["action"] = "stop"


def test_execution_audit_event_defensively_copies_details():
    details = {
        "action": "reconcile",
    }

    event = ExecutionAuditEvent(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details=details,
        sequence_number=1,
    )

    details["action"] = "stop"

    assert event.details["action"] == "reconcile"


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_audit_event_id",
        "execution_intent_id",
    ],
)
def test_execution_audit_event_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_audit_event_id": "AUDIT-001",
        "execution_intent_id": "INTENT-001",
        "execution_result_id": None,
        "event_type": ExecutionAuditEventType.INTENT_RECEIVED,
        "occurred_at": datetime.now(timezone.utc),
        "details": {},
        "sequence_number": 1,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionAuditEvent(**values)


def test_execution_audit_event_rejects_invalid_event_type():
    with pytest.raises(TypeError):
        ExecutionAuditEvent(
            execution_audit_event_id="AUDIT-001",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type="INTENT_RECEIVED",
            occurred_at=datetime.now(timezone.utc),
            details={},
            sequence_number=1,
        )


def test_execution_audit_event_rejects_missing_occurred_at():
    with pytest.raises(ValueError):
        ExecutionAuditEvent(
            execution_audit_event_id="AUDIT-001",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type=ExecutionAuditEventType.INTENT_RECEIVED,
            occurred_at=None,
            details={},
            sequence_number=1,
        )


@pytest.mark.parametrize(
    "sequence_number",
    [
        0,
        -1,
    ],
)
def test_execution_audit_event_rejects_non_positive_sequence(
    sequence_number,
):
    with pytest.raises(ValueError):
        ExecutionAuditEvent(
            execution_audit_event_id="AUDIT-001",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type=ExecutionAuditEventType.INTENT_RECEIVED,
            occurred_at=datetime.now(timezone.utc),
            details={},
            sequence_number=sequence_number,
        )


def test_execution_audit_event_rejects_non_integer_sequence():
    with pytest.raises(TypeError):
        ExecutionAuditEvent(
            execution_audit_event_id="AUDIT-001",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type=ExecutionAuditEventType.INTENT_RECEIVED,
            occurred_at=datetime.now(timezone.utc),
            details={},
            sequence_number="1",
        )


def test_execution_result_id_may_be_present():
    event = ExecutionAuditEvent(
        execution_audit_event_id="AUDIT-002",
        execution_intent_id="INTENT-001",
        execution_result_id="RESULT-001",
        event_type=ExecutionAuditEventType.EXECUTION_SUCCEEDED,
        occurred_at=datetime.now(timezone.utc),
        details={},
        sequence_number=3,
    )

    assert event.execution_result_id == "RESULT-001"


def test_execution_result_id_rejects_empty_text():
    with pytest.raises(ValueError):
        ExecutionAuditEvent(
            execution_audit_event_id="AUDIT-002",
            execution_intent_id="INTENT-001",
            execution_result_id="",
            event_type=ExecutionAuditEventType.EXECUTION_SUCCEEDED,
            occurred_at=datetime.now(timezone.utc),
            details={},
            sequence_number=3,
        )