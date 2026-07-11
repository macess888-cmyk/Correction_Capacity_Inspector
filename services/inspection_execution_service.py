from __future__ import annotations

from models.execution_transition_operation import (
    ExecutionTransitionOperation,
)
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
from services.execution_transition_coordinator import (
    ExecutionTransitionCoordinator,
)
from services.execution_transition_factory import (
    ExecutionTransitionFactory,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)


class InspectionExecutionService:
    """
    Facade for inspection execution lifecycle operations.

    Execution creation remains an explicit lifecycle-origin action.

    Every subsequent lifecycle transition is derived from the
    execution grammar and delegated to the consistency coordinator.

    This service contains no transition policy, state-mutation,
    compensation, or event-construction logic.
    """

    def __init__(
        self,
        registry: InspectionExecutionRegistry,
        event_service: InspectionExecutionEventService,
        transition_factory: ExecutionTransitionFactory,
        transition_coordinator: ExecutionTransitionCoordinator,
    ) -> None:
        self._registry = registry
        self._event_service = event_service
        self._transition_factory = transition_factory
        self._transition_coordinator = transition_coordinator

    def create_execution(
        self,
        execution: InspectionExecution,
        event_id: str,
    ) -> InspectionExecution:
        """
        Register a new execution and record its lifecycle origin.

        Creation is not a state transition. The execution begins
        in CREATED and the corresponding event records that origin.
        """

        self._registry.add(execution)

        event = InspectionExecutionEvent(
            event_id=event_id,
            execution_id=execution.execution_id,
            event_type=(
                InspectionExecutionEventType.EXECUTION_CREATED
            ),
            previous_status=InspectionExecutionStatus.CREATED,
            current_status=InspectionExecutionStatus.CREATED,
            stage=execution.current_stage,
            message="Execution created.",
        )

        self._event_service.record_event(event)

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
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.INITIALIZE,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def start_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.START,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def pause_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.PAUSE,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def resume_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.RESUME,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def complete_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.COMPLETE,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def fail_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
        failure_reason: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.FAIL,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
            message="Execution failed.",
            metadata={
                "failure_reason": failure_reason,
            },
        )

    def cancel_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.CANCEL,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def archive_execution(
        self,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
    ) -> InspectionExecution:
        return self._coordinate_transition(
            operation=ExecutionTransitionOperation.ARCHIVE,
            execution_id=execution_id,
            transition_id=transition_id,
            event_id=event_id,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

    def list_events_for_execution(
        self,
        execution_id: str,
    ) -> list[InspectionExecutionEvent]:
        return self._event_service.list_events_for_execution(
            execution_id
        )

    def _coordinate_transition(
        self,
        operation: ExecutionTransitionOperation,
        execution_id: str,
        transition_id: str,
        event_id: str,
        receipt_id: str,
        consistency_record_id: str,
        message: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> InspectionExecution:
        execution = self._registry.get(execution_id)

        intent = self._transition_factory.build_transition(
            operation=operation,
            transition_id=transition_id,
            execution_id=execution_id,
            event_id=event_id,
            previous_status=execution.status,
            message=message,
            metadata=metadata,
        )

        self._transition_coordinator.coordinate(
            intent=intent,
            receipt_id=receipt_id,
            consistency_record_id=consistency_record_id,
        )

        return self._registry.get(execution_id)