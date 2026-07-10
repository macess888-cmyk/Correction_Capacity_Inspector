from __future__ import annotations

from models.inspection_execution import InspectionExecution


class InspectionExecutionRegistry:
    """
    Mutable registry for InspectionExecution objects.

    Registry invariants:
    - Execution identifiers must be unique.
    - Duplicate additions raise ValueError.
    - Missing reads, updates, and removals raise KeyError.
    """

    def __init__(self) -> None:
        self._executions: dict[str, InspectionExecution] = {}

    def add(
        self,
        execution: InspectionExecution,
    ) -> None:
        execution_id = execution.execution_id

        if execution_id in self._executions:
            raise ValueError(
                f"Inspection execution already exists: {execution_id}"
            )

        self._executions[execution_id] = execution

    def get(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        if execution_id not in self._executions:
            raise KeyError(
                f"Inspection execution not found: {execution_id}"
            )

        return self._executions[execution_id]

    def update(
        self,
        execution: InspectionExecution,
    ) -> None:
        execution_id = execution.execution_id

        if execution_id not in self._executions:
            raise KeyError(
                f"Inspection execution not found: {execution_id}"
            )

        self._executions[execution_id] = execution

    def remove(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        if execution_id not in self._executions:
            raise KeyError(
                f"Inspection execution not found: {execution_id}"
            )

        return self._executions.pop(execution_id)

    def exists(
        self,
        execution_id: str,
    ) -> bool:
        return execution_id in self._executions

    def list(
        self,
    ) -> list[InspectionExecution]:
        return list(self._executions.values())

    def count(self) -> int:
        return len(self._executions)