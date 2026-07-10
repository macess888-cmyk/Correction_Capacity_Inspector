from __future__ import annotations

from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from registries.inspection_execution_event_registry import (
    InspectionExecutionEventRegistry,
)


class InspectionExecutionEventService:
    """
    Provides append-only access to execution events.

    This service records and retrieves immutable events.

    It does not update, remove, reinterpret,
    or authorize execution behavior.
    """

    def __init__(
        self,
        registry: InspectionExecutionEventRegistry,
    ) -> None:
        self._registry = registry

    def record_event(
        self,
        event: InspectionExecutionEvent,
    ) -> None:
        self._registry.add(event)

    def get_event(
        self,
        event_id: str,
    ) -> InspectionExecutionEvent:
        return self._registry.get(event_id)

    def event_exists(
        self,
        event_id: str,
    ) -> bool:
        return self._registry.exists(event_id)

    def list_events(
        self,
    ) -> list[InspectionExecutionEvent]:
        return self._registry.list()

    def list_events_for_execution(
        self,
        execution_id: str,
    ) -> list[InspectionExecutionEvent]:
        return self._registry.list_for_execution(
            execution_id
        )

    def count_events(self) -> int:
        return self._registry.count()

    def count_events_for_execution(
        self,
        execution_id: str,
    ) -> int:
        return self._registry.count_for_execution(
            execution_id
        )