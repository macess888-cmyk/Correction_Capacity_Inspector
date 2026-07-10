import pytest

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
from services.execution_consistency_service import (
    ExecutionConsistencyService,
)


def make_service() -> ExecutionConsistencyService:
    return ExecutionConsistencyService(
        intent_registry=ExecutionTransitionIntentRegistry(),
        receipt_registry=ExecutionTransitionReceiptRegistry(),
        consistency_registry=ExecutionConsistencyRecordRegistry(),
    )


def make_intent(
    transition_id: str = "transition-001",
    execution_id: str = "execution-001",
) -> ExecutionTransitionIntent:
    return ExecutionTransitionIntent(
        transition_id=transition_id,
        execution_id=execution_id,
        event_id=f"event-{transition_id}",
        previous_status=InspectionExecutionStatus.INITIALIZED,
        target_status=InspectionExecutionStatus.RUNNING,
        event_type=(
            InspectionExecutionEventType.EXECUTION_STARTED
        ),
        target_stage="RUNNING",
    )


def make_receipt(
    receipt_id: str = "receipt-001",
    execution_id: str = "execution-001",
) -> ExecutionTransitionReceipt:
    return ExecutionTransitionReceipt(
        receipt_id=receipt_id,
        transition_id=f"transition-{receipt_id}",
        execution_id=execution_id,
        state_updated=True,
        event_recorded=True,
        consistency_status=(
            ExecutionConsistencyStatus.CONSISTENT
        ),
    )


def make_record(
    record_id: str = "record-001",
    execution_id: str = "execution-001",
) -> ExecutionConsistencyRecord:
    return ExecutionConsistencyRecord(
        record_id=record_id,
        transition_id=f"transition-{record_id}",
        execution_id=execution_id,
        consistency_status=(
            ExecutionConsistencyStatus.RECOVERY_REQUIRED
        ),
        expected_status=InspectionExecutionStatus.RUNNING,
        observed_status=InspectionExecutionStatus.INITIALIZED,
        expected_event_id=f"event-{record_id}",
        failure_stage="EVENT_RECORDING",
        failure_reason="Event persistence failed.",
    )


def test_service_records_and_gets_intent() -> None:
    service = make_service()
    intent = make_intent()

    service.record_intent(intent)

    assert service.get_intent("transition-001") is intent
    assert service.intent_exists("transition-001") is True
    assert service.list_intents() == [intent]


def test_service_lists_intents_for_execution() -> None:
    service = make_service()

    first = make_intent(
        "transition-001",
        "execution-001",
    )
    second = make_intent(
        "transition-002",
        "execution-002",
    )
    third = make_intent(
        "transition-003",
        "execution-001",
    )

    service.record_intent(first)
    service.record_intent(second)
    service.record_intent(third)

    assert service.list_intents_for_execution(
        "execution-001"
    ) == [first, third]


def test_service_records_and_gets_receipt() -> None:
    service = make_service()
    receipt = make_receipt()

    service.record_receipt(receipt)

    assert service.get_receipt("receipt-001") is receipt
    assert service.receipt_exists("receipt-001") is True
    assert service.list_receipts() == [receipt]


def test_service_lists_receipts_for_execution() -> None:
    service = make_service()

    first = make_receipt(
        "receipt-001",
        "execution-001",
    )
    second = make_receipt(
        "receipt-002",
        "execution-002",
    )
    third = make_receipt(
        "receipt-003",
        "execution-001",
    )

    service.record_receipt(first)
    service.record_receipt(second)
    service.record_receipt(third)

    assert service.list_receipts_for_execution(
        "execution-001"
    ) == [first, third]


def test_service_records_and_gets_consistency_issue() -> None:
    service = make_service()
    record = make_record()

    service.record_consistency_issue(record)

    assert service.get_consistency_issue("record-001") is record
    assert service.consistency_issue_exists("record-001") is True
    assert service.list_consistency_issues() == [record]


def test_service_lists_consistency_issues_for_execution() -> None:
    service = make_service()

    first = make_record(
        "record-001",
        "execution-001",
    )
    second = make_record(
        "record-002",
        "execution-002",
    )
    third = make_record(
        "record-003",
        "execution-001",
    )

    service.record_consistency_issue(first)
    service.record_consistency_issue(second)
    service.record_consistency_issue(third)

    assert service.list_consistency_issues_for_execution(
        "execution-001"
    ) == [first, third]


@pytest.mark.parametrize(
    ("record_method", "item"),
    [
        (
            "record_intent",
            make_intent(),
        ),
        (
            "record_receipt",
            make_receipt(),
        ),
        (
            "record_consistency_issue",
            make_record(),
        ),
    ],
)
def test_service_rejects_duplicate_identifiers(
    record_method: str,
    item: object,
) -> None:
    service = make_service()
    record = getattr(service, record_method)

    record(item)

    with pytest.raises(ValueError):
        record(item)


def test_service_exposes_no_update_or_remove_operations() -> None:
    service = make_service()

    assert not hasattr(service, "update_intent")
    assert not hasattr(service, "remove_intent")
    assert not hasattr(service, "update_receipt")
    assert not hasattr(service, "remove_receipt")
    assert not hasattr(service, "update_consistency_issue")
    assert not hasattr(service, "remove_consistency_issue")