from __future__ import annotations

from datetime import UTC, datetime

from models.inspection_execution import InspectionExecution
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.inspection_execution_transition_policy import (
    InspectionExecutionTransitionPolicy,
)


class InspectionExecutionService:
    """
    Manages inspection execution lifecycle transitions.

    Every status change must pass through the verified transition
    policy. This service contains no inspection decision logic,
    scoring, inference, or execution authority.
    """

    def __init__(
        self,
        registry: InspectionExecutionRegistry,
    ) -> None:
        self._registry = registry

    def create_execution(
        self,
        execution: InspectionExecution,
    ) -> None:
        self._registry.add(execution)

    def get_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._registry.get(execution_id)

    def list_executions(
        self,
    ) -> list[InspectionExecution]:
        return self._registry.list()

    def execution_exists(
        self,
        execution_id: str,
    ) -> bool:
        return self._registry.exists(execution_id)

    def count_executions(self) -> int:
        return self._registry.count()

    def initialize_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id,
            InspectionExecutionStatus.INITIALIZED,
            current_stage="INITIALIZED",
        )

    def start_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id,
            InspectionExecutionStatus.RUNNING,
            current_stage="RUNNING",
        )

    def pause_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id,
            InspectionExecutionStatus.PAUSED,
            current_stage="PAUSED",
        )

    def resume_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id,
            InspectionExecutionStatus.RUNNING,
            current_stage="RUNNING",
        )

    def complete_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        execution = self._transition(
            execution_id,
            InspectionExecutionStatus.COMPLETED,
            current_stage="COMPLETED",
        )

        execution.completed = datetime.now(UTC)
        self._registry.update(execution)

        return execution

    def fail_execution(
        self,
        execution_id: str,
        failure_reason: str,
    ) -> InspectionExecution:
        execution = self._transition(
            execution_id,
            InspectionExecutionStatus.FAILED,
            current_stage="FAILED",
        )

        execution.failure_reason = failure_reason
        execution.completed = datetime.now(UTC)
        self._registry.update(execution)

        return execution

    def cancel_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        execution = self._transition(
            execution_id,
            InspectionExecutionStatus.CANCELLED,
            current_stage="CANCELLED",
        )

        execution.completed = datetime.now(UTC)
        self._registry.update(execution)

        return execution

    def archive_execution(
        self,
        execution_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id,
            InspectionExecutionStatus.ARCHIVED,
            current_stage="ARCHIVED",
        )

    def _transition(
        self,
        execution_id: str,
        target: InspectionExecutionStatus,
        current_stage: str,
    ) -> InspectionExecution:
        execution = self._registry.get(execution_id)

        InspectionExecutionTransitionPolicy.validate_transition(
            execution.status,
            target,
        )

        execution.status = target
        execution.current_stage = current_stage

        self._registry.update(execution)

        return execution