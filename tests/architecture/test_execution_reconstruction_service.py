from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)
from models.execution_consistency_status import (
    ExecutionConsistencyStatus,
)
from models.execution_evidence_completeness import (
    ExecutionEvidenceCompleteness,
)
from models.execution_reconstruction_integrity import (
    ExecutionReconstructionIntegrity,
)
from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_receipt import (
    ExecutionTransitionReceipt,
)
from models.inspection_execution_event import (
    InspectionExecutionEvent,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from services.execution_reconstruction_service import (
    ExecutionReconstructionService,
)


def make_intent(
    transition_id: str,
    event_id: str,
    previous_status: InspectionExecutionStatus,
    target_status: InspectionExecutionStatus,
    event_type: InspectionExecutionEventType,
    stage: str,
) -> ExecutionTransitionIntent:
    return ExecutionTransitionIntent(
        transition_id=transition_id,
        execution_id="execution-001",
        event_id=event_id,
        previous_status=previous_status,
        target_status=target_status,
        event_type=event_type,
        target_stage=stage,
    )


def make_event(
    event_id: str,
    previous_status: InspectionExecutionStatus,
    current_status: InspectionExecutionStatus,
    event_type: InspectionExecutionEventType,
    stage: str,
) -> InspectionExecutionEvent:
    return InspectionExecutionEvent(
        event_id=event_id,
        execution_id="execution-001",
        event_type=event_type,
        previous_status=previous_status,
        current_status=current_status,
        stage=stage,
    )


def make_receipt(
    receipt_id: str,
    transition_id: str,
) -> ExecutionTransitionReceipt:
    return ExecutionTransitionReceipt(
        receipt_id=receipt_id,
        transition_id=transition_id,
        execution_id="execution-001",
        state_updated=True,
        event_recorded=True,
        consistency_status=(
            ExecutionConsistencyStatus.CONSISTENT
        ),
    )


def test_service_reconstructs_complete_consistent_execution() -> None:
    service = ExecutionReconstructionService()

    intents = [
        make_intent(
            transition_id="transition-001",
            event_id="event-001",
            previous_status=InspectionExecutionStatus.CREATED,
            target_status=InspectionExecutionStatus.INITIALIZED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_INITIALIZED
            ),
            stage="INITIALIZED",
        ),
        make_intent(
            transition_id="transition-002",
            event_id="event-002",
            previous_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            target_status=InspectionExecutionStatus.RUNNING,
            event_type=(
                InspectionExecutionEventType.EXECUTION_STARTED
            ),
            stage="RUNNING",
        ),
        make_intent(
            transition_id="transition-003",
            event_id="event-003",
            previous_status=InspectionExecutionStatus.RUNNING,
            target_status=InspectionExecutionStatus.COMPLETED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_COMPLETED
            ),
            stage="COMPLETED",
        ),
    ]

    events = [
        make_event(
            event_id="event-001",
            previous_status=InspectionExecutionStatus.CREATED,
            current_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            event_type=(
                InspectionExecutionEventType.EXECUTION_INITIALIZED
            ),
            stage="INITIALIZED",
        ),
        make_event(
            event_id="event-002",
            previous_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            current_status=InspectionExecutionStatus.RUNNING,
            event_type=(
                InspectionExecutionEventType.EXECUTION_STARTED
            ),
            stage="RUNNING",
        ),
        make_event(
            event_id="event-003",
            previous_status=InspectionExecutionStatus.RUNNING,
            current_status=InspectionExecutionStatus.COMPLETED,
            event_type=(
                InspectionExecutionEventType.EXECUTION_COMPLETED
            ),
            stage="COMPLETED",
        ),
    ]

    receipts = [
        make_receipt("receipt-001", "transition-001"),
        make_receipt("receipt-002", "transition-002"),
        make_receipt("receipt-003", "transition-003"),
    ]

    reconstruction = service.reconstruct(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        intents=intents,
        events=events,
        receipts=receipts,
        consistency_records=[],
    )

    assert reconstruction.reconstructed_status == (
        InspectionExecutionStatus.COMPLETED
    )
    assert reconstruction.reconstructed_stage == "COMPLETED"
    assert reconstruction.operations_applied == (
        "EXECUTION_INITIALIZED",
        "EXECUTION_STARTED",
        "EXECUTION_COMPLETED",
    )
    assert reconstruction.evidence_processed == 9
    assert reconstruction.integrity == (
        ExecutionReconstructionIntegrity.CONSISTENT
    )
    assert reconstruction.completeness == (
        ExecutionEvidenceCompleteness.COMPLETE
    )
    assert reconstruction.warnings == ()


def test_service_returns_insufficient_without_events() -> None:
    service = ExecutionReconstructionService()

    reconstruction = service.reconstruct(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        intents=[],
        events=[],
        receipts=[],
        consistency_records=[],
    )

    assert reconstruction.reconstructed_status == (
        InspectionExecutionStatus.CREATED
    )
    assert reconstruction.reconstructed_stage == "NOT_STARTED"
    assert reconstruction.integrity == (
        ExecutionReconstructionIntegrity.UNKNOWN
    )
    assert reconstruction.completeness == (
        ExecutionEvidenceCompleteness.INSUFFICIENT
    )
    assert reconstruction.warnings == (
        "No execution events were available.",
    )


def test_service_marks_partial_transition_evidence() -> None:
    service = ExecutionReconstructionService()

    intent = make_intent(
        transition_id="transition-001",
        event_id="event-001",
        previous_status=InspectionExecutionStatus.CREATED,
        target_status=InspectionExecutionStatus.INITIALIZED,
        event_type=(
            InspectionExecutionEventType.EXECUTION_INITIALIZED
        ),
        stage="INITIALIZED",
    )

    events = [
        make_event(
            event_id="event-001",
            previous_status=InspectionExecutionStatus.CREATED,
            current_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            event_type=(
                InspectionExecutionEventType.EXECUTION_INITIALIZED
            ),
            stage="INITIALIZED",
        ),
        make_event(
            event_id="event-002",
            previous_status=(
                InspectionExecutionStatus.INITIALIZED
            ),
            current_status=InspectionExecutionStatus.RUNNING,
            event_type=(
                InspectionExecutionEventType.EXECUTION_STARTED
            ),
            stage="RUNNING",
        ),
    ]

    reconstruction = service.reconstruct(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        intents=[intent],
        events=events,
        receipts=[
            make_receipt(
                "receipt-001",
                "transition-001",
            )
        ],
        consistency_records=[],
    )

    assert reconstruction.completeness == (
        ExecutionEvidenceCompleteness.PARTIAL
    )
    assert "Transition evidence was incomplete." in (
        reconstruction.warnings
    )


def test_service_marks_consistency_records_as_inconsistent() -> None:
    service = ExecutionReconstructionService()

    event = make_event(
        event_id="event-001",
        previous_status=InspectionExecutionStatus.CREATED,
        current_status=InspectionExecutionStatus.INITIALIZED,
        event_type=(
            InspectionExecutionEventType.EXECUTION_INITIALIZED
        ),
        stage="INITIALIZED",
    )

    record = ExecutionConsistencyRecord(
        record_id="record-001",
        transition_id="transition-001",
        execution_id="execution-001",
        consistency_status=(
            ExecutionConsistencyStatus.RECOVERY_REQUIRED
        ),
        expected_status=InspectionExecutionStatus.RUNNING,
        observed_status=InspectionExecutionStatus.INITIALIZED,
        expected_event_id="event-002",
        failure_stage="EVENT_RECORDING",
        failure_reason="Event persistence failed.",
    )

    reconstruction = service.reconstruct(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        intents=[],
        events=[event],
        receipts=[],
        consistency_records=[record],
    )

    assert reconstruction.integrity == (
        ExecutionReconstructionIntegrity.INCONSISTENT
    )
    assert "One or more consistency records were present." in (
        reconstruction.warnings
    )


def test_service_filters_evidence_by_execution_id() -> None:
    service = ExecutionReconstructionService()

    target_event = make_event(
        event_id="event-001",
        previous_status=InspectionExecutionStatus.CREATED,
        current_status=InspectionExecutionStatus.INITIALIZED,
        event_type=(
            InspectionExecutionEventType.EXECUTION_INITIALIZED
        ),
        stage="INITIALIZED",
    )

    other_event = InspectionExecutionEvent(
        event_id="event-other",
        execution_id="execution-other",
        event_type=(
            InspectionExecutionEventType.EXECUTION_COMPLETED
        ),
        previous_status=InspectionExecutionStatus.RUNNING,
        current_status=InspectionExecutionStatus.COMPLETED,
        stage="COMPLETED",
    )

    reconstruction = service.reconstruct(
        execution_id="execution-001",
        grammar_version="v1.4.0",
        intents=[],
        events=[other_event, target_event],
        receipts=[],
        consistency_records=[],
    )

    assert reconstruction.reconstructed_status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert reconstruction.evidence_processed == 1