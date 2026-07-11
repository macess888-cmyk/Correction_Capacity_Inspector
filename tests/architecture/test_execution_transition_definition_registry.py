from dataclasses import FrozenInstanceError

import pytest

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


def test_operation_vocabulary_is_closed() -> None:
    assert {
        operation.value
        for operation in ExecutionTransitionOperation
    } == {
        "INITIALIZE",
        "START",
        "PAUSE",
        "RESUME",
        "COMPLETE",
        "FAIL",
        "CANCEL",
        "ARCHIVE",
    }


def test_registry_contains_all_operations() -> None:
    registry = ExecutionTransitionDefinitionRegistry()

    assert registry.count() == 8

    assert {
        definition.operation
        for definition in registry.list()
    } == set(ExecutionTransitionOperation)


@pytest.mark.parametrize(
    (
        "operation",
        "target_status",
        "event_type",
        "target_stage",
        "default_message",
    ),
    [
        (
            ExecutionTransitionOperation.INITIALIZE,
            InspectionExecutionStatus.INITIALIZED,
            InspectionExecutionEventType.EXECUTION_INITIALIZED,
            "INITIALIZED",
            "Execution initialized.",
        ),
        (
            ExecutionTransitionOperation.START,
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionEventType.EXECUTION_STARTED,
            "RUNNING",
            "Execution started.",
        ),
        (
            ExecutionTransitionOperation.PAUSE,
            InspectionExecutionStatus.PAUSED,
            InspectionExecutionEventType.EXECUTION_PAUSED,
            "PAUSED",
            "Execution paused.",
        ),
        (
            ExecutionTransitionOperation.RESUME,
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionEventType.EXECUTION_RESUMED,
            "RUNNING",
            "Execution resumed.",
        ),
        (
            ExecutionTransitionOperation.COMPLETE,
            InspectionExecutionStatus.COMPLETED,
            InspectionExecutionEventType.EXECUTION_COMPLETED,
            "COMPLETED",
            "Execution completed.",
        ),
        (
            ExecutionTransitionOperation.FAIL,
            InspectionExecutionStatus.FAILED,
            InspectionExecutionEventType.EXECUTION_FAILED,
            "FAILED",
            "Execution failed.",
        ),
        (
            ExecutionTransitionOperation.CANCEL,
            InspectionExecutionStatus.CANCELLED,
            InspectionExecutionEventType.EXECUTION_CANCELLED,
            "CANCELLED",
            "Execution cancelled.",
        ),
        (
            ExecutionTransitionOperation.ARCHIVE,
            InspectionExecutionStatus.ARCHIVED,
            InspectionExecutionEventType.EXECUTION_ARCHIVED,
            "ARCHIVED",
            "Execution archived.",
        ),
    ],
)
def test_registry_returns_expected_definition(
    operation: ExecutionTransitionOperation,
    target_status: InspectionExecutionStatus,
    event_type: InspectionExecutionEventType,
    target_stage: str,
    default_message: str,
) -> None:
    registry = ExecutionTransitionDefinitionRegistry()

    definition = registry.get(operation)

    assert definition.operation == operation
    assert definition.target_status == target_status
    assert definition.event_type == event_type
    assert definition.target_stage == target_stage
    assert definition.default_message == default_message


def test_definitions_are_immutable() -> None:
    registry = ExecutionTransitionDefinitionRegistry()

    definition = registry.get(
        ExecutionTransitionOperation.START
    )

    with pytest.raises(FrozenInstanceError):
        definition.target_stage = "CHANGED"  # type: ignore[misc]


def test_registry_is_read_only() -> None:
    registry = ExecutionTransitionDefinitionRegistry()

    assert not hasattr(registry, "add")
    assert not hasattr(registry, "update")
    assert not hasattr(registry, "remove")