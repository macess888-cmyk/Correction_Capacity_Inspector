from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)
from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)
from models.inspection_execution import InspectionExecution
from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.execution_consistency_service import (
    ExecutionConsistencyService,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)
from services.inspection_execution_transition_policy import (
    InspectionExecutionTransitionPolicy,
)


class ExecutionTransitionCoordinator:
    """
    Coordinates one inspectable execution transition boundary.

    Responsibilities:

    - Record transition intent.
    - Validate the intent against current execution state.
    - Validate transition policy.
    - Perform preflight checks.
    - Mutate current execution state.
    - Record the corresponding immutable event.
    - Attempt compensation if event recording fails.
    - Record an immutable transition receipt.
    - Record unresolved or compensated consistency issues.

    The coordinator does not make inspection decisions,
    establish truth, or authorize domain action.
    """

    def __init__(
        self,
        execution_registry: InspectionExecutionRegistry,
        event_service: InspectionExecutionEventService,
        consistency_service: ExecutionConsistencyService,
    ) -> None:
        self._execution_registry = execution_registry
        self._event_service = event_service
        self._consistency_service = consistency_service

    def coordinate(
        self,
        intent: ExecutionTransitionIntent,
        receipt_id: str,
        consistency_record_id: str,
    ) -> ExecutionTransitionReceipt:
        """
        Attempt one state-and-event transition boundary.

        Every attempt records an intent.

        Every handled outcome records a receipt.
        """

        self._consistency_service.record_intent(intent)

        execution = self._execution_registry.get(
            intent.execution_id
        )

        self._validate_intent_matches_execution(
            intent=intent,
            execution=execution,
        )

        InspectionExecutionTransitionPolicy.validate_transition(
            execution.status,
            intent.target_status,
        )

        if self._event_service.event_exists(intent.event_id):
            receipt = ExecutionTransitionReceipt(
                receipt_id=receipt_id,
                transition_id=intent.transition_id,
                execution_id=intent.execution_id,
                state_updated=False,
                event_recorded=False,
                consistency_status=(
                    ExecutionConsistencyStatus.STATE_NOT_UPDATED
                ),
                failure_stage="PREFLIGHT",
                failure_reason=(
                    "Execution event identifier already exists: "
                    f"{intent.event_id}"
                ),
            )

            self._consistency_service.record_receipt(receipt)

            return receipt

        previous_snapshot = replace(execution)

        execution.status = intent.target_status
        execution.current_stage = intent.target_stage

        if intent.target_status.value in {
            "COMPLETED",
            "FAILED",
            "CANCELLED",
        }:
            execution.completed = datetime.now(UTC)

        failure_reason = str(
            intent.metadata.get("failure_reason", "")
        )

        if failure_reason:
            execution.failure_reason = failure_reason

        self._execution_registry.update(execution)

        event = InspectionExecutionEvent(
            event_id=intent.event_id,
            execution_id=intent.execution_id,
            event_type=intent.event_type,
            previous_status=intent.previous_status,
            current_status=intent.target_status,
            stage=intent.target_stage,
            message=intent.message,
            metadata=intent.metadata,
        )

        try:
            self._event_service.record_event(event)
        except Exception as error:
            return self._handle_event_recording_failure(
                intent=intent,
                receipt_id=receipt_id,
                consistency_record_id=consistency_record_id,
                previous_snapshot=previous_snapshot,
                error=error,
            )

        receipt = ExecutionTransitionReceipt(
            receipt_id=receipt_id,
            transition_id=intent.transition_id,
            execution_id=intent.execution_id,
            state_updated=True,
            event_recorded=True,
            consistency_status=(
                ExecutionConsistencyStatus.CONSISTENT
            ),
        )

        self._consistency_service.record_receipt(receipt)

        return receipt

    def _validate_intent_matches_execution(
        self,
        intent: ExecutionTransitionIntent,
        execution: InspectionExecution,
    ) -> None:
        if execution.status != intent.previous_status:
            raise ValueError(
                "Transition intent previous status does not match "
                "current execution status: "
                f"{intent.previous_status.value} != "
                f"{execution.status.value}"
            )

    def _handle_event_recording_failure(
        self,
        intent: ExecutionTransitionIntent,
        receipt_id: str,
        consistency_record_id: str,
        previous_snapshot: InspectionExecution,
        error: Exception,
    ) -> ExecutionTransitionReceipt:
        compensation_attempted = True
        compensation_succeeded = False

        try:
            self._execution_registry.update(
                previous_snapshot
            )
            compensation_succeeded = True
        except Exception:
            compensation_succeeded = False

        current_execution = self._execution_registry.get(
            intent.execution_id
        )

        consistency_status = (
            ExecutionConsistencyStatus.COMPENSATED
            if compensation_succeeded
            else ExecutionConsistencyStatus.RECOVERY_REQUIRED
        )

        record = ExecutionConsistencyRecord(
            record_id=consistency_record_id,
            transition_id=intent.transition_id,
            execution_id=intent.execution_id,
            consistency_status=consistency_status,
            expected_status=intent.target_status,
            observed_status=current_execution.status,
            expected_event_id=intent.event_id,
            failure_stage="EVENT_RECORDING",
            failure_reason=str(error),
            compensation_attempted=compensation_attempted,
            compensation_succeeded=compensation_succeeded,
        )

        self._consistency_service.record_consistency_issue(
            record
        )

        receipt = ExecutionTransitionReceipt(
            receipt_id=receipt_id,
            transition_id=intent.transition_id,
            execution_id=intent.execution_id,
            state_updated=not compensation_succeeded,
            event_recorded=False,
            consistency_status=consistency_status,
            failure_stage="EVENT_RECORDING",
            failure_reason=str(error),
            metadata={
                "compensation_attempted": (
                    compensation_attempted
                ),
                "compensation_succeeded": (
                    compensation_succeeded
                ),
                "consistency_record_id": (
                    consistency_record_id
                ),
            },
        )

        self._consistency_service.record_receipt(receipt)

        return receipt