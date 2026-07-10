from __future__ import annotations

from models.inspection_execution_event import (
    InspectionExecutionEvent,
)


class InspectionExecutionEventRegistry:
    """
    Append-only registry for InspectionExecutionEvent objects.

    Registry invariants:
    - Event identifiers must be unique.
    - Events may be added and retrieved.
    - Existing events cannot be updated or removed.
    - Missing reads raise KeyError.
    """

    def __init__(self) -> None:
        self._events: dict[
            str,
            InspectionExecutionEvent,
        ] = {}

    def add(
        self,
        event: InspectionExecutionEvent,
    ) -> None:
        if event.event_id in self._events:
            raise ValueError(
                "Inspection execution event already exists: "
                f"{event.event_id}"
            )

        self._events[event.event_id] = event

    def get(
        self,
        event_id: str,
    ) -> InspectionExecutionEvent:
        if event_id not in self._events:
            raise KeyError(
                "Inspection execution event not found: "
                f"{event_id}"
            )

        return self._events[event_id]

    def exists(
        self,
        event_id: str,
    ) -> bool:
        return event_id in self._events

    def list(
        self,
    ) -> list[InspectionExecutionEvent]:
        return list(self._events.values())

    def list_for_execution(
        self,
        execution_id: str,
    ) -> list[InspectionExecutionEvent]:
        return [
            event
            for event in self._events.values()
            if event.execution_id == execution_id
        ]

    def count(self) -> int:
        return len(self._events)

    def count_for_execution(
        self,
        execution_id: str,
    ) -> int:
        return len(
            self.list_for_execution(execution_id)
        )