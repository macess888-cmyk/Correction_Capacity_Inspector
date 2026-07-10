from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Mapping

from models.inspection_execution import InspectionExecution
from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)
from services.inspection_execution_transition_policy import (
    InspectionExecutionTransitionPolicy,
)


class InspectionExecutionService:
    """
    Manages inspection execution lifecycle transitions.

    Every status change must pass through the verified transition
    policy and record exactly one immutable execution event.

    This service contains no inspection decision logic,
    scoring, inference, or execution authority.
    """

    def __init__(
        self,
        registry: InspectionExecutionRegistry,
        event_service: InspectionExecutionEventService,
    ) -> None:
        self._registry = registry
        self._event_service = event_service

    def create_execution(
        self,
        execution: InspectionExecution,
        event_id: str,
    ) -> InspectionExecution:
        self._registry.add(execution)

        self._record_event(
            event_id=event_id,
            execution=execution,
            event_type=(
                InspectionExecutionEventType.EXECUTION_CREATED
            ),
            previous_status=InspectionExecutionStatus.CREATED,
            current_status=InspectionExecutionStatus.CREATED,
            message="Execution created.",
        )

        return execution

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
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.INITIALIZED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_INITIALIZED
            ),
            current_stage="INITIALIZED",
            message="Execution initialized.",
        )

    def start_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.RUNNING,
            event_type=(
                InspectionExecutionEventType.EXECUTION_STARTED
            ),
            current_stage="RUNNING",
            message="Execution started.",
        )

    def pause_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.PAUSED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_PAUSED
            ),
            current_stage="PAUSED",
            message="Execution paused.",
        )

    def resume_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.RUNNING,
            event_type=(
                InspectionExecutionEventType.EXECUTION_RESUMED
            ),
            current_stage="RUNNING",
            message="Execution resumed.",
        )

    def complete_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.COMPLETED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_COMPLETED
            ),
            current_stage="COMPLETED",
            message="Execution completed.",
            mark_completed=True,
        )

    def fail_execution(
        self,
        execution_id: str,
        event_id: str,
        failure_reason: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.FAILED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_FAILED
            ),
            current_stage="FAILED",
            message="Execution failed.",
            failure_reason=failure_reason,
            mark_completed=True,
            metadata={
                "failure_reason": failure_reason,
            },
        )

    def cancel_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.CANCELLED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_CANCELLED
            ),
            current_stage="CANCELLED",
            message="Execution cancelled.",
            mark_completed=True,
        )

    def archive_execution(
        self,
        execution_id: str,
        event_id: str,
    ) -> InspectionExecution:
        return self._transition(
            execution_id=execution_id,
            event_id=event_id,
            target=InspectionExecutionStatus.ARCHIVED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_ARCHIVED
            ),
            current_stage="ARCHIVED",
            message="Execution archived.",
        )

    def list_events_for_execution(
        self,
        execution_id: str,
    ) -> list[InspectionExecutionEvent]:
        return self._event_service.list_events_for_execution(
            execution_id
        )

    def _transition(
        self,
        execution_id: str,
        event_id: str,
        target: InspectionExecutionStatus,
        event_type: InspectionExecutionEventType,
        current_stage: str,
        message: str,
        failure_reason: str = "",
        mark_completed: bool = False,
        metadata: Mapping[str, Any] | None = None,
    ) -> InspectionExecution:
        execution = self._registry.get(execution_id)
        previous_status = execution.status

        InspectionExecutionTransitionPolicy.validate_transition(
            previous_status,
            target,
        )

        execution.status = target
        execution.current_stage = current_stage

        if failure_reason:
            execution.failure_reason = failure_reason

        if mark_completed:
            execution.completed = datetime.now(UTC)

        self._registry.update(execution)

        self._record_event(
            event_id=event_id,
            execution=execution,
            event_type=event_type,
            previous_status=previous_status,
            current_status=target,
            message=message,
            metadata=metadata,
        )

        return execution

    def _record_event(
        self,
        event_id: str,
        execution: InspectionExecution,
        event_type: InspectionExecutionEventType,
        previous_status: InspectionExecutionStatus,
        current_status: InspectionExecutionStatus,
        message: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        event = InspectionExecutionEvent(
            event_id=event_id,
            execution_id=execution.execution_id,
            event_type=event_type,
            previous_status=previous_status,
            current_status=current_status,
            stage=execution.current_stage,
            message=message,
            metadata=metadata or {},
        )

        self._event_service.record_event(event)