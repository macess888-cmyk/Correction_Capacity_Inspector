from dataclasses import FrozenInstanceError

import pytest

from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)
from models.execution_plan import ExecutionPlan
from models.execution_plan_status import ExecutionPlanStatus
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)


def build_plan() -> ExecutionPlan:

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="STOPPED",
        status=ExecutionDivergenceStatus.DIVERGED,
    )

    inspection = ExecutionInspection(
        execution_id="exec-001",
        divergence=divergence,
        status=ExecutionInspectionStatus.INCONSISTENT,
        observations=(),
        requires_attention=True,
    )

    recommendation = ExecutionRecommendation(
        execution_id="exec-001",
        inspection=inspection,
        status=ExecutionRecommendationStatus.AVAILABLE,
        recommendation_type=ExecutionRecommendationType.VERIFY_RUNTIME,
        reason="Verify runtime.",
    )

    return ExecutionPlan(
        execution_id="exec-001",
        recommendation=recommendation,
        status=ExecutionPlanStatus.AVAILABLE,
    )


def test_execution_authorization_model():

    plan = build_plan()

    authorization = ExecutionAuthorization(
        execution_id="exec-001",
        plan=plan,
        status=ExecutionAuthorizationStatus.PENDING,
        reason="Awaiting authorization.",
    )

    assert authorization.execution_id == "exec-001"
    assert authorization.plan == plan
    assert (
        authorization.status
        == ExecutionAuthorizationStatus.PENDING
    )
    assert authorization.reason == "Awaiting authorization."


def test_execution_authorization_is_frozen():

    plan = build_plan()

    authorization = ExecutionAuthorization(
        execution_id="exec-001",
        plan=plan,
        status=ExecutionAuthorizationStatus.PENDING,
        reason="Awaiting authorization.",
    )

    with pytest.raises(FrozenInstanceError):
        authorization.execution_id = "changed"