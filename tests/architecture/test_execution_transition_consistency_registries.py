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


@pytest.mark.parametrize(
    ("registry", "item", "identifier", "get_name", "exists_name"),
    [
        (
            ExecutionTransitionIntentRegistry(),
            make_intent(),
            "transition-001",
            "get",
            "exists",
        ),
        (
            ExecutionTransitionReceiptRegistry(),
            make_receipt(),
            "receipt-001",
            "get",
            "exists",
        ),
        (
            ExecutionConsistencyRecordRegistry(),
            make_record(),
            "record-001",
            "get",
            "exists",
        ),
    ],
)
def test_registry_add_get_exists_and_count(
    registry: object,
    item: object,
    identifier: str,
    get_name: str,
    exists_name: str,
) -> None:
    add = getattr(registry, "add")
    get = getattr(registry, get_name)
    exists = getattr(registry, exists_name)
    count = getattr(registry, "count")

    add(item)

    assert get(identifier) is item
    assert exists(identifier) is True
    assert count() == 1


def test_intent_registry_lists_for_execution() -> None:
    registry = ExecutionTransitionIntentRegistry()

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

    registry.add(first)
    registry.add(second)
    registry.add(third)

    assert registry.list_for_execution(
        "execution-001"
    ) == [first, third]


def test_receipt_registry_lists_for_execution() -> None:
    registry = ExecutionTransitionReceiptRegistry()

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

    registry.add(first)
    registry.add(second)
    registry.add(third)

    assert registry.list_for_execution(
        "execution-001"
    ) == [first, third]


def test_consistency_registry_lists_for_execution() -> None:
    registry = ExecutionConsistencyRecordRegistry()

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

    registry.add(first)
    registry.add(second)
    registry.add(third)

    assert registry.list_for_execution(
        "execution-001"
    ) == [first, third]


@pytest.mark.parametrize(
    ("registry", "item"),
    [
        (
            ExecutionTransitionIntentRegistry(),
            make_intent(),
        ),
        (
            ExecutionTransitionReceiptRegistry(),
            make_receipt(),
        ),
        (
            ExecutionConsistencyRecordRegistry(),
            make_record(),
        ),
    ],
)
def test_registry_rejects_duplicate_identifier(
    registry: object,
    item: object,
) -> None:
    add = getattr(registry, "add")

    add(item)

    with pytest.raises(ValueError):
        add(item)


@pytest.mark.parametrize(
    "registry",
    [
        ExecutionTransitionIntentRegistry(),
        ExecutionTransitionReceiptRegistry(),
        ExecutionConsistencyRecordRegistry(),
    ],
)
def test_registry_missing_get_raises_key_error(
    registry: object,
) -> None:
    get = getattr(registry, "get")

    with pytest.raises(KeyError):
        get("missing")


@pytest.mark.parametrize(
    "registry",
    [
        ExecutionTransitionIntentRegistry(),
        ExecutionTransitionReceiptRegistry(),
        ExecutionConsistencyRecordRegistry(),
    ],
)
def test_registry_exposes_no_mutation_surface(
    registry: object,
) -> None:
    assert not hasattr(registry, "update")
    assert not hasattr(registry, "remove")