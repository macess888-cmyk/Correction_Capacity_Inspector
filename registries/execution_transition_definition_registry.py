from __future__ import annotations

from models.execution_transition_definition import (
    ExecutionTransitionDefinition,
)
from models.execution_transition_operation import (
    ExecutionTransitionOperation,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


class ExecutionTransitionDefinitionRegistry:
    """
    Read-only registry for immutable execution transition definitions.

    The registry is the execution grammar dictionary.

    Definitions may be inspected and retrieved,
    but not added, updated, or removed at runtime.
    """

    def __init__(self) -> None:
        self._definitions: dict[
            ExecutionTransitionOperation,
            ExecutionTransitionDefinition,
        ] = {
            ExecutionTransitionOperation.INITIALIZE: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.INITIALIZE
                    ),
                    target_status=(
                        InspectionExecutionStatus.INITIALIZED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_INITIALIZED
                    ),
                    target_stage="INITIALIZED",
                    default_message="Execution initialized.",
                )
            ),
            ExecutionTransitionOperation.START: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.START
                    ),
                    target_status=(
                        InspectionExecutionStatus.RUNNING
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_STARTED
                    ),
                    target_stage="RUNNING",
                    default_message="Execution started.",
                )
            ),
            ExecutionTransitionOperation.PAUSE: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.PAUSE
                    ),
                    target_status=(
                        InspectionExecutionStatus.PAUSED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_PAUSED
                    ),
                    target_stage="PAUSED",
                    default_message="Execution paused.",
                )
            ),
            ExecutionTransitionOperation.RESUME: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.RESUME
                    ),
                    target_status=(
                        InspectionExecutionStatus.RUNNING
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_RESUMED
                    ),
                    target_stage="RUNNING",
                    default_message="Execution resumed.",
                )
            ),
            ExecutionTransitionOperation.COMPLETE: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.COMPLETE
                    ),
                    target_status=(
                        InspectionExecutionStatus.COMPLETED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_COMPLETED
                    ),
                    target_stage="COMPLETED",
                    default_message="Execution completed.",
                )
            ),
            ExecutionTransitionOperation.FAIL: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.FAIL
                    ),
                    target_status=(
                        InspectionExecutionStatus.FAILED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_FAILED
                    ),
                    target_stage="FAILED",
                    default_message="Execution failed.",
                )
            ),
            ExecutionTransitionOperation.CANCEL: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.CANCEL
                    ),
                    target_status=(
                        InspectionExecutionStatus.CANCELLED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_CANCELLED
                    ),
                    target_stage="CANCELLED",
                    default_message="Execution cancelled.",
                )
            ),
            ExecutionTransitionOperation.ARCHIVE: (
                ExecutionTransitionDefinition(
                    operation=(
                        ExecutionTransitionOperation.ARCHIVE
                    ),
                    target_status=(
                        InspectionExecutionStatus.ARCHIVED
                    ),
                    event_type=(
                        InspectionExecutionEventType
                        .EXECUTION_ARCHIVED
                    ),
                    target_stage="ARCHIVED",
                    default_message="Execution archived.",
                )
            ),
        }

    def get(
        self,
        operation: ExecutionTransitionOperation,
    ) -> ExecutionTransitionDefinition:
        if operation not in self._definitions:
            raise KeyError(
                f"Transition definition not found: {operation}"
            )

        return self._definitions[operation]

    def exists(
        self,
        operation: ExecutionTransitionOperation,
    ) -> bool:
        return operation in self._definitions

    def list(
        self,
    ) -> list[ExecutionTransitionDefinition]:
        return list(self._definitions.values())

    def count(self) -> int:
        return len(self._definitions)