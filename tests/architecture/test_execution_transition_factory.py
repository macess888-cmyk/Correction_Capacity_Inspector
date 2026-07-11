from models.execution_transition_operation import (
    ExecutionTransitionOperation,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.execution_transition_definition_registry import (
    ExecutionTransitionDefinitionRegistry,
)
from services.execution_transition_factory import (
    ExecutionTransitionFactory,
)


def make_factory() -> ExecutionTransitionFactory:
    return ExecutionTransitionFactory(
        ExecutionTransitionDefinitionRegistry()
    )


def test_factory_builds_start_intent_from_definition() -> None:
    factory = make_factory()

    intent = factory.build_transition(
        operation=ExecutionTransitionOperation.START,
        transition_id="transition-001",
        execution_id="execution-001",
        event_id="event-001",
        previous_status=(
            InspectionExecutionStatus.INITIALIZED
        ),
    )

    assert intent.transition_id == "transition-001"
    assert intent.execution_id == "execution-001"
    assert intent.event_id == "event-001"
    assert intent.previous_status == (
        InspectionExecutionStatus.INITIALIZED
    )
    assert intent.target_status == (
        InspectionExecutionStatus.RUNNING
    )
    assert intent.event_type == (
        InspectionExecutionEventType.EXECUTION_STARTED
    )
    assert intent.target_stage == "RUNNING"
    assert intent.message == "Execution started."
    assert intent.metadata == {}


def test_factory_supports_custom_message_and_metadata() -> None:
    factory = make_factory()

    intent = factory.build_transition(
        operation=ExecutionTransitionOperation.FAIL,
        transition_id="transition-002",
        execution_id="execution-001",
        event_id="event-002",
        previous_status=InspectionExecutionStatus.RUNNING,
        message="Report persistence failed.",
        metadata={
            "failure_reason": "Report persistence failed.",
        },
    )

    assert intent.target_status == (
        InspectionExecutionStatus.FAILED
    )
    assert intent.event_type == (
        InspectionExecutionEventType.EXECUTION_FAILED
    )
    assert intent.target_stage == "FAILED"
    assert intent.message == "Report persistence failed."
    assert intent.metadata == {
        "failure_reason": "Report persistence failed.",
    }


def test_factory_uses_default_message_only_when_none() -> None:
    factory = make_factory()

    intent = factory.build_transition(
        operation=ExecutionTransitionOperation.PAUSE,
        transition_id="transition-003",
        execution_id="execution-001",
        event_id="event-003",
        previous_status=InspectionExecutionStatus.RUNNING,
        message="",
    )

    assert intent.message == ""


def test_factory_builds_all_operations() -> None:
    factory = make_factory()

    expected = {
        ExecutionTransitionOperation.INITIALIZE: (
            InspectionExecutionStatus.INITIALIZED
        ),
        ExecutionTransitionOperation.START: (
            InspectionExecutionStatus.RUNNING
        ),
        ExecutionTransitionOperation.PAUSE: (
            InspectionExecutionStatus.PAUSED
        ),
        ExecutionTransitionOperation.RESUME: (
            InspectionExecutionStatus.RUNNING
        ),
        ExecutionTransitionOperation.COMPLETE: (
            InspectionExecutionStatus.COMPLETED
        ),
        ExecutionTransitionOperation.FAIL: (
            InspectionExecutionStatus.FAILED
        ),
        ExecutionTransitionOperation.CANCEL: (
            InspectionExecutionStatus.CANCELLED
        ),
        ExecutionTransitionOperation.ARCHIVE: (
            InspectionExecutionStatus.ARCHIVED
        ),
    }

    for index, (operation, target_status) in enumerate(
        expected.items(),
        start=1,
    ):
        intent = factory.build_transition(
            operation=operation,
            transition_id=f"transition-{index}",
            execution_id="execution-001",
            event_id=f"event-{index}",
            previous_status=InspectionExecutionStatus.CREATED,
        )

        assert intent.target_status == target_status


def test_factory_copies_metadata_through_immutable_intent() -> None:
    factory = make_factory()

    metadata = {
        "source": "original",
    }

    intent = factory.build_transition(
        operation=ExecutionTransitionOperation.INITIALIZE,
        transition_id="transition-004",
        execution_id="execution-001",
        event_id="event-004",
        previous_status=InspectionExecutionStatus.CREATED,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert intent.metadata["source"] == "original"