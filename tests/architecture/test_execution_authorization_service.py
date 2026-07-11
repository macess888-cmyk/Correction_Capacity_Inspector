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
from services.execution_authorization_service import (
    ExecutionAuthorizationService,
)


def build_plan(status: ExecutionPlanStatus) -> ExecutionPlan:

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
        status=status,
    )


def test_available_plan_produces_pending_authorization():

    service = ExecutionAuthorizationService()

    plan = build_plan(ExecutionPlanStatus.AVAILABLE)

    authorization = service.authorize(plan)

    assert authorization.execution_id == "exec-001"
    assert (
        authorization.status
        == ExecutionAuthorizationStatus.PENDING
    )
    assert authorization.reason == "Execution plan awaits authorization."


def test_incomplete_plan_is_not_authorized():

    service = ExecutionAuthorizationService()

    plan = build_plan(ExecutionPlanStatus.INCOMPLETE)

    authorization = service.authorize(plan)

    assert (
        authorization.status
        == ExecutionAuthorizationStatus.NOT_AUTHORIZED
    )
    assert (
        authorization.reason
        == "Incomplete execution plans cannot be authorized."
    )


def test_not_plannable_plan_is_not_authorized():

    service = ExecutionAuthorizationService()

    plan = build_plan(ExecutionPlanStatus.NOT_PLANNABLE)

    authorization = service.authorize(plan)

    assert (
        authorization.status
        == ExecutionAuthorizationStatus.NOT_AUTHORIZED
    )
    assert (
        authorization.reason
        == "Non-plannable execution plans cannot be authorized."
    )


def test_unknown_plan_produces_unknown_authorization():

    service = ExecutionAuthorizationService()

    plan = build_plan(ExecutionPlanStatus.UNKNOWN)

    authorization = service.authorize(plan)

    assert (
        authorization.status
        == ExecutionAuthorizationStatus.UNKNOWN
    )
    assert authorization.reason == "Authorization could not be determined."