from datetime import datetime, timezone

import pytest

from models.execution_audit_event_type import ExecutionAuditEventType
from services.execution_audit_trail import ExecutionAuditTrail


def test_audit_trail_records_first_event():
    trail = ExecutionAuditTrail()

    event = trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={
            "action": "reconcile",
        },
    )

    assert event.sequence_number == 1
    assert event.execution_audit_event_id == "AUDIT-001"
    assert event.execution_intent_id == "INTENT-001"


def test_audit_trail_assigns_monotonic_sequence_numbers():
    trail = ExecutionAuditTrail()

    first = trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    second = trail.record_event(
        execution_audit_event_id="AUDIT-002",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.EXECUTION_STARTED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    assert first.sequence_number == 1
    assert second.sequence_number == 2


def test_audit_trail_returns_events_in_recorded_order():
    trail = ExecutionAuditTrail()

    trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    trail.record_event(
        execution_audit_event_id="AUDIT-002",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.EXECUTION_STARTED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    events = trail.events()

    assert [event.execution_audit_event_id for event in events] == [
        "AUDIT-001",
        "AUDIT-002",
    ]


def test_audit_trail_returns_immutable_snapshot():
    trail = ExecutionAuditTrail()

    trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    events = trail.events()

    assert isinstance(events, tuple)

    with pytest.raises(AttributeError):
        events.append("invalid")


def test_audit_trail_filters_by_intent():
    trail = ExecutionAuditTrail()

    trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    trail.record_event(
        execution_audit_event_id="AUDIT-002",
        execution_intent_id="INTENT-002",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    events = trail.events_for_intent("INTENT-001")

    assert len(events) == 1
    assert events[0].execution_intent_id == "INTENT-001"


def test_audit_trail_rejects_empty_intent_filter():
    trail = ExecutionAuditTrail()

    with pytest.raises(ValueError):
        trail.events_for_intent("")


def test_audit_trail_rejects_duplicate_event_id():
    trail = ExecutionAuditTrail()

    trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    with pytest.raises(ValueError):
        trail.record_event(
            execution_audit_event_id="AUDIT-001",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type=ExecutionAuditEventType.EXECUTION_STARTED,
            occurred_at=datetime.now(timezone.utc),
            details={},
        )


def test_audit_trail_preserves_result_reference():
    trail = ExecutionAuditTrail()

    event = trail.record_event(
        execution_audit_event_id="AUDIT-003",
        execution_intent_id="INTENT-001",
        execution_result_id="RESULT-001",
        event_type=ExecutionAuditEventType.EXECUTION_SUCCEEDED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    assert event.execution_result_id == "RESULT-001"


def test_audit_trail_preserves_model_validation():
    trail = ExecutionAuditTrail()

    with pytest.raises(ValueError):
        trail.record_event(
            execution_audit_event_id="",
            execution_intent_id="INTENT-001",
            execution_result_id=None,
            event_type=ExecutionAuditEventType.INTENT_RECEIVED,
            occurred_at=datetime.now(timezone.utc),
            details={},
        )


def test_audit_trail_does_not_expose_mutable_internal_storage():
    trail = ExecutionAuditTrail()

    snapshot = trail.events()

    trail.record_event(
        execution_audit_event_id="AUDIT-001",
        execution_intent_id="INTENT-001",
        execution_result_id=None,
        event_type=ExecutionAuditEventType.INTENT_RECEIVED,
        occurred_at=datetime.now(timezone.utc),
        details={},
    )

    assert snapshot == ()
    assert len(trail.events()) == 1