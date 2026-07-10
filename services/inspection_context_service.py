from __future__ import annotations

from datetime import UTC, datetime

from models.inspection_context import InspectionContext
from registries.inspection_context_registry import (
    InspectionContextRegistry,
)


class InspectionContextService:
    """
    Service responsible for managing the lifecycle
    of InspectionContext objects.

    This service contains no inspection logic,
    scoring, reasoning, or authority.
    """

    def __init__(
        self,
        registry: InspectionContextRegistry,
    ) -> None:
        self._registry = registry

    def create_context(
        self,
        context: InspectionContext,
    ) -> None:
        self._registry.add(context)

    def get_context(
        self,
        inspection_id: str,
    ) -> InspectionContext:
        return self._registry.get(inspection_id)

    def update_context(
        self,
        context: InspectionContext,
    ) -> None:
        self._registry.update(context)

    def complete_context(
        self,
        inspection_id: str,
    ) -> InspectionContext:
        context = self._registry.get(inspection_id)

        context.status = "COMPLETED"
        context.completed = datetime.now(UTC)

        self._registry.update(context)

        return context

    def pause_context(
        self,
        inspection_id: str,
    ) -> InspectionContext:
        context = self._registry.get(inspection_id)

        context.status = "PAUSED"

        self._registry.update(context)

        return context

    def resume_context(
        self,
        inspection_id: str,
    ) -> InspectionContext:
        context = self._registry.get(inspection_id)

        context.status = "ACTIVE"

        self._registry.update(context)

        return context

    def archive_context(
        self,
        inspection_id: str,
    ) -> InspectionContext:
        context = self._registry.get(inspection_id)

        context.status = "ARCHIVED"

        self._registry.update(context)

        return context

    def list_contexts(
        self,
    ) -> list[InspectionContext]:
        return self._registry.list()

    def context_exists(
        self,
        inspection_id: str,
    ) -> bool:
        return self._registry.exists(inspection_id)

    def count_contexts(
        self,
    ) -> int:
        return self._registry.count()