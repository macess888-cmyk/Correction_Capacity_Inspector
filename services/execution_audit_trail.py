from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from models.execution_audit_event import ExecutionAuditEvent
from models.execution_audit_event_type import ExecutionAuditEventType


class ExecutionAuditTrail:
    """Stores immutable execution audit events in recorded order."""

    def __init__(self) -> None:
        self._events: list[ExecutionAuditEvent] = []
        self._event_ids: set[str] = set()

    def record_event(
        self,
        *,
        execution_audit_event_id: str,
        execution_intent_id: str,
        execution_result_id: str | None,
        event_type: ExecutionAuditEventType,
        occurred_at: datetime,
        details: Mapping[str, Any],
    ) -> ExecutionAuditEvent:
        if execution_audit_event_id in self._event_ids:
            raise ValueError(
                "execution_audit_event_id must be unique"
            )

        event = ExecutionAuditEvent(
            execution_audit_event_id=execution_audit_event_id,
            execution_intent_id=execution_intent_id,
            execution_result_id=execution_result_id,
            event_type=event_type,
            occurred_at=occurred_at,
            details=details,
            sequence_number=len(self._events) + 1,
        )

        self._events.append(event)
        self._event_ids.add(execution_audit_event_id)

        return event

    def events(self) -> tuple[ExecutionAuditEvent, ...]:
        return tuple(self._events)

    def events_for_intent(
        self,
        execution_intent_id: str,
    ) -> tuple[ExecutionAuditEvent, ...]:
        if not isinstance(execution_intent_id, str):
            raise TypeError(
                "execution_intent_id must be a string"
            )

        if not execution_intent_id.strip():
            raise ValueError(
                "execution_intent_id must not be empty"
            )

        return tuple(
            event
            for event in self._events
            if event.execution_intent_id == execution_intent_id
        )