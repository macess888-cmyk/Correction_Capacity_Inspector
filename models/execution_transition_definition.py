from __future__ import annotations

from dataclasses import dataclass

from models.execution_transition_operation import (
    ExecutionTransitionOperation,
)
from models.inspection_execution_event_type import (
    InspectionExecutionEventType,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


@dataclass(frozen=True, slots=True)
class ExecutionTransitionDefinition:
    """
    Immutable semantic definition of one execution operation.

    A definition describes architectural meaning only.

    It contains no runtime identity, mutable execution state,
    timestamps, receipts, or consistency outcomes.
    """

    operation: ExecutionTransitionOperation

    target_status: InspectionExecutionStatus
    event_type: InspectionExecutionEventType

    target_stage: str
    default_message: str