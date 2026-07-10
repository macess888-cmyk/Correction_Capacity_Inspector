import pytest

from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.inspection_execution import InspectionExecution
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.execution_consistency_record_registry import (
    ExecutionConsistencyRecordRegistry,
)
from registries.execution_transition_intent_registry import (
    ExecutionTransitionIntentRegistry,
)
from registries.execution_transition_receipt_registry import (
    ExecutionTransitionReceiptRegistry,
)
from registries.inspection_execution_event_registry import (
    InspectionExecutionEventRegistry,
)
from registries.inspection_execution_registry import (
    InspectionExecutionRegistry,
)
from services.execution_consistency_service import (
    ExecutionConsistencyService,
)
from services.execution_transition_coordinator import (
    ExecutionTransitionCoordinator,
)
from services.inspection_execution_event_service import (
    InspectionExecutionEventService,
)


class FailingEventService(InspectionExecutionEventService):
    def record_event(self, event) -> None:
        raise RuntimeError("Event persistence failed.")


class FailingCompensationRegistry(InspectionExecutionRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._update_calls = 0

    def update(self, execution: InspectionExecution) -> None:
        self._update_calls += 1

        if self._update_calls >= 2:
            raise RuntimeError("Compensation failed.")

        super().update(execution)


def make_consistency_service() -> ExecutionConsistencyService:
    return ExecutionConsistencyService(
        intent_registry=ExecutionTransitionIntentRegistry(),
        receipt_registry=ExecutionTransitionReceiptRegistry(),
        consistency_registry=ExecutionConsistencyRecordRegistry(),
    )


def make_intent(
    transition_id: str = "transition-001",
    event_id: str = "event-001",
) -> ExecutionTransitionIntent:
    return ExecutionTransitionIntent(
        transition_id=transition_id,
        execution_id="execution-001",
        event_id=event_id,
        previous_status=InspectionExecutionStatus.INITIALIZED,
        target_status=InspectionExecutionStatus.RUNNING,
        event_type=(
            InspectionExecutionEventType.EXECUTION_STARTED
        ),
        target_stage="RUNNING",
        message="Execution started.",
    )


def make_execution_registry() -> InspectionExecutionRegistry:
    registry = InspectionExecutionRegistry()

    registry.add(
        InspectionExecution(
            execution_id="execution-001",
            inspection_id="inspection-001",
            status=InspectionExecutionStatus.INITIALIZED,
            current_stage="INITIALIZED",
        )
    )

    return registry


def test_coordinator_records_consistent_transition() -> None:
    execution_registry = make_execution_registry()
    event_service = InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )
    consistency_service = make_consistency_service()

    coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    receipt = coordinator.coordinate(
        intent=make_intent(),
        receipt_id="receipt-001",
        consistency_record_id="record-001",
    )

    execution = execution_registry.get("execution-001")

    assert execution.status == InspectionExecutionStatus.RUNNING
    assert execution.current_stage == "RUNNING"

    assert receipt.consistency_status == (
        ExecutionConsistencyStatus.CONSISTENT
    )
    assert receipt.state_updated is True
    assert receipt.event_recorded is True

    assert event_service.event_exists("event-001") is True
    assert consistency_service.intent_exists(
        "transition-001"
    ) is True
    assert consistency_service.receipt_exists(
        "receipt-001"
    ) is True
    assert consistency_service.list_consistency_issues() == []


def test_coordinator_preflight_duplicate_event_avoids_state_change() -> None:
    execution_registry = make_execution_registry()
    event_service = InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )
    consistency_service = make_consistency_service()

    event_service.record_event(
        __import__(
            "models.inspection_execution_event",
            fromlist=["InspectionExecutionEvent"],
        ).InspectionExecutionEvent(
            event_id="event-existing",
            execution_id="other-execution",
            event_type=(
                InspectionExecutionEventType.EXECUTION_STARTED
            ),
            previous_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            current_status=InspectionExecutionStatus.RUNNING,
            stage="RUNNING",
        )
    )

    coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    receipt = coordinator.coordinate(
        intent=make_intent(event_id="event-existing"),
        receipt_id="receipt-001",
        consistency_record_id="record-001",
    )

    execution = execution_registry.get("execution-001")

    assert execution.status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert receipt.consistency_status == (
        ExecutionConsistencyStatus.STATE_NOT_UPDATED
    )
    assert receipt.state_updated is False
    assert receipt.event_recorded is False


def test_coordinator_compensates_when_event_recording_fails() -> None:
    execution_registry = make_execution_registry()
    event_service = FailingEventService(
        InspectionExecutionEventRegistry()
    )
    consistency_service = make_consistency_service()

    coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    receipt = coordinator.coordinate(
        intent=make_intent(),
        receipt_id="receipt-001",
        consistency_record_id="record-001",
    )

    execution = execution_registry.get("execution-001")
    records = consistency_service.list_consistency_issues()

    assert execution.status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert receipt.consistency_status == (
        ExecutionConsistencyStatus.COMPENSATED
    )
    assert receipt.state_updated is False
    assert receipt.event_recorded is False

    assert len(records) == 1
    assert records[0].compensation_attempted is True
    assert records[0].compensation_succeeded is True


def test_coordinator_records_recovery_required_when_compensation_fails() -> None:
    execution_registry = FailingCompensationRegistry()

    execution_registry.add(
        InspectionExecution(
            execution_id="execution-001",
            inspection_id="inspection-001",
            status=InspectionExecutionStatus.INITIALIZED,
            current_stage="INITIALIZED",
        )
    )

    event_service = FailingEventService(
        InspectionExecutionEventRegistry()
    )
    consistency_service = make_consistency_service()

    coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    receipt = coordinator.coordinate(
        intent=make_intent(),
        receipt_id="receipt-001",
        consistency_record_id="record-001",
    )

    records = consistency_service.list_consistency_issues()

    assert receipt.consistency_status == (
        ExecutionConsistencyStatus.RECOVERY_REQUIRED
    )
    assert receipt.state_updated is True
    assert receipt.event_recorded is False

    assert len(records) == 1
    assert records[0].compensation_attempted is True
    assert records[0].compensation_succeeded is False


def test_coordinator_rejects_stale_previous_status() -> None:
    execution_registry = make_execution_registry()
    event_service = InspectionExecutionEventService(
        InspectionExecutionEventRegistry()
    )
    consistency_service = make_consistency_service()

    coordinator = ExecutionTransitionCoordinator(
        execution_registry=execution_registry,
        event_service=event_service,
        consistency_service=consistency_service,
    )

    stale_intent = ExecutionTransitionIntent(
        transition_id="transition-stale",
        execution_id="execution-001",
        event_id="event-stale",
        previous_status=InspectionExecutionStatus.CREATED,
        target_status=InspectionExecutionStatus.INITIALIZED,
        event_type=(
            InspectionExecutionEventType.EXECUTION_INITIALIZED
        ),
        target_stage="INITIALIZED",
    )

    with pytest.raises(
        ValueError,
        match="previous status does not match",
    ):
        coordinator.coordinate(
            intent=stale_intent,
            receipt_id="receipt-stale",
            consistency_record_id="record-stale",
        )