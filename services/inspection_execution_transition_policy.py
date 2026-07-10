from __future__ import annotations

from models.inspection_execution_status import (
    InspectionExecutionStatus,
)


class InspectionExecutionTransitionPolicy:
    """
    Defines and validates allowed execution-state transitions.

    The policy contains lifecycle rules only.
    It does not mutate executions or authorize inspection action.
    """

    _ALLOWED_TRANSITIONS: dict[
        InspectionExecutionStatus,
        frozenset[InspectionExecutionStatus],
    ] = {
        InspectionExecutionStatus.CREATED: frozenset(
            {
                InspectionExecutionStatus.INITIALIZED,
                InspectionExecutionStatus.CANCELLED,
            }
        ),
        InspectionExecutionStatus.INITIALIZED: frozenset(
            {
                InspectionExecutionStatus.RUNNING,
                InspectionExecutionStatus.CANCELLED,
            }
        ),
        InspectionExecutionStatus.RUNNING: frozenset(
            {
                InspectionExecutionStatus.PAUSED,
                InspectionExecutionStatus.COMPLETED,
                InspectionExecutionStatus.FAILED,
                InspectionExecutionStatus.CANCELLED,
            }
        ),
        InspectionExecutionStatus.PAUSED: frozenset(
            {
                InspectionExecutionStatus.RUNNING,
                InspectionExecutionStatus.CANCELLED,
            }
        ),
        InspectionExecutionStatus.COMPLETED: frozenset(
            {
                InspectionExecutionStatus.ARCHIVED,
            }
        ),
        InspectionExecutionStatus.FAILED: frozenset(
            {
                InspectionExecutionStatus.ARCHIVED,
            }
        ),
        InspectionExecutionStatus.CANCELLED: frozenset(
            {
                InspectionExecutionStatus.ARCHIVED,
            }
        ),
        InspectionExecutionStatus.ARCHIVED: frozenset(),
    }

    @classmethod
    def can_transition(
        cls,
        current: InspectionExecutionStatus,
        target: InspectionExecutionStatus,
    ) -> bool:
        return target in cls._ALLOWED_TRANSITIONS[current]

    @classmethod
    def validate_transition(
        cls,
        current: InspectionExecutionStatus,
        target: InspectionExecutionStatus,
    ) -> None:
        if not cls.can_transition(current, target):
            raise ValueError(
                "Invalid inspection execution transition: "
                f"{current.value} -> {target.value}"
            )

    @classmethod
    def allowed_targets(
        cls,
        current: InspectionExecutionStatus,
    ) -> frozenset[InspectionExecutionStatus]:
        return cls._ALLOWED_TRANSITIONS[current]