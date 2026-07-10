from __future__ import annotations

from models.inspection_context import InspectionContext


class InspectionContextRegistry:
    """
    Mutable registry for InspectionContext objects.

    Registry invariants:
    - Context identifiers must be unique.
    - Duplicate additions raise ValueError.
    - Missing reads, updates, and removals raise KeyError.
    """

    def __init__(self) -> None:
        self._contexts: dict[str, InspectionContext] = {}

    def add(self, context: InspectionContext) -> None:
        inspection_id = context.inspection_id

        if inspection_id in self._contexts:
            raise ValueError(
                f"Inspection context already exists: {inspection_id}"
            )

        self._contexts[inspection_id] = context

    def get(self, inspection_id: str) -> InspectionContext:
        if inspection_id not in self._contexts:
            raise KeyError(
                f"Inspection context not found: {inspection_id}"
            )

        return self._contexts[inspection_id]

    def update(self, context: InspectionContext) -> None:
        inspection_id = context.inspection_id

        if inspection_id not in self._contexts:
            raise KeyError(
                f"Inspection context not found: {inspection_id}"
            )

        self._contexts[inspection_id] = context

    def remove(self, inspection_id: str) -> InspectionContext:
        if inspection_id not in self._contexts:
            raise KeyError(
                f"Inspection context not found: {inspection_id}"
            )

        return self._contexts.pop(inspection_id)

    def exists(self, inspection_id: str) -> bool:
        return inspection_id in self._contexts

    def list(self) -> list[InspectionContext]:
        return list(self._contexts.values())

    def count(self) -> int:
        return len(self._contexts)