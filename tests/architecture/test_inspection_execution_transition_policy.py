import pytest

from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from services.inspection_execution_transition_policy import (
    InspectionExecutionTransitionPolicy,
)


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (
            InspectionExecutionStatus.CREATED,
            InspectionExecutionStatus.INITIALIZED,
        ),
        (
            InspectionExecutionStatus.CREATED,
            InspectionExecutionStatus.CANCELLED,
        ),
        (
            InspectionExecutionStatus.INITIALIZED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.INITIALIZED,
            InspectionExecutionStatus.CANCELLED,
        ),
        (
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionStatus.PAUSED,
        ),
        (
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionStatus.COMPLETED,
        ),
        (
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionStatus.FAILED,
        ),
        (
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionStatus.CANCELLED,
        ),
        (
            InspectionExecutionStatus.PAUSED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.PAUSED,
            InspectionExecutionStatus.CANCELLED,
        ),
        (
            InspectionExecutionStatus.COMPLETED,
            InspectionExecutionStatus.ARCHIVED,
        ),
        (
            InspectionExecutionStatus.FAILED,
            InspectionExecutionStatus.ARCHIVED,
        ),
        (
            InspectionExecutionStatus.CANCELLED,
            InspectionExecutionStatus.ARCHIVED,
        ),
    ],
)
def test_allowed_transitions_are_accepted(
    current: InspectionExecutionStatus,
    target: InspectionExecutionStatus,
) -> None:
    assert (
        InspectionExecutionTransitionPolicy.can_transition(
            current,
            target,
        )
        is True
    )

    InspectionExecutionTransitionPolicy.validate_transition(
        current,
        target,
    )


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (
            InspectionExecutionStatus.CREATED,
            InspectionExecutionStatus.COMPLETED,
        ),
        (
            InspectionExecutionStatus.CREATED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.INITIALIZED,
            InspectionExecutionStatus.COMPLETED,
        ),
        (
            InspectionExecutionStatus.RUNNING,
            InspectionExecutionStatus.INITIALIZED,
        ),
        (
            InspectionExecutionStatus.PAUSED,
            InspectionExecutionStatus.COMPLETED,
        ),
        (
            InspectionExecutionStatus.COMPLETED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.FAILED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.CANCELLED,
            InspectionExecutionStatus.RUNNING,
        ),
        (
            InspectionExecutionStatus.ARCHIVED,
            InspectionExecutionStatus.CREATED,
        ),
        (
            InspectionExecutionStatus.ARCHIVED,
            InspectionExecutionStatus.RUNNING,
        ),
    ],
)
def test_invalid_transitions_raise_value_error(
    current: InspectionExecutionStatus,
    target: InspectionExecutionStatus,
) -> None:
    assert (
        InspectionExecutionTransitionPolicy.can_transition(
            current,
            target,
        )
        is False
    )

    with pytest.raises(
        ValueError,
        match=(
            "Invalid inspection execution transition: "
            f"{current.value} -> {target.value}"
        ),
    ):
        InspectionExecutionTransitionPolicy.validate_transition(
            current,
            target,
        )


def test_allowed_targets_returns_exact_transition_set() -> None:
    allowed = (
        InspectionExecutionTransitionPolicy.allowed_targets(
            InspectionExecutionStatus.RUNNING
        )
    )

    assert allowed == frozenset(
        {
            InspectionExecutionStatus.PAUSED,
            InspectionExecutionStatus.COMPLETED,
            InspectionExecutionStatus.FAILED,
            InspectionExecutionStatus.CANCELLED,
        }
    )


def test_archived_state_has_no_allowed_targets() -> None:
    allowed = (
        InspectionExecutionTransitionPolicy.allowed_targets(
            InspectionExecutionStatus.ARCHIVED
        )
    )

    assert allowed == frozenset()