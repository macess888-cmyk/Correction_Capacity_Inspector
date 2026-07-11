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
from models.execution_readiness_status import (
    ExecutionReadinessStatus,
)
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)
from services.execution_readiness_service import (
    ExecutionReadinessService,
)


def build_authorization(
    status: ExecutionAuthorizationStatus,
) -> ExecutionAuthorization:

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

    plan = ExecutionPlan(
        execution_id="exec-001",
        recommendation=recommendation,
        status=ExecutionPlanStatus.AVAILABLE,
    )

    return ExecutionAuthorization(
        execution_id="exec-001",
        plan=plan,
        status=status,
        reason="Test authorization.",
    )


def test_pending_authorization_is_not_ready():

    service = ExecutionReadinessService()

    authorization = build_authorization(
        ExecutionAuthorizationStatus.PENDING
    )

    readiness = service.assess(authorization)

    assert readiness.execution_id == "exec-001"
    assert readiness.status == ExecutionReadinessStatus.NOT_READY
    assert (
        readiness.reason
        == "Execution authorization is still pending."
    )


def test_not_authorized_execution_is_blocked():

    service = ExecutionReadinessService()

    authorization = build_authorization(
        ExecutionAuthorizationStatus.NOT_AUTHORIZED
    )

    readiness = service.assess(authorization)

    assert readiness.status == ExecutionReadinessStatus.BLOCKED
    assert (
        readiness.reason
        == "Execution is blocked because authorization was not granted."
    )


def test_authorized_execution_is_ready():

    service = ExecutionReadinessService()

    authorization = build_authorization(
        ExecutionAuthorizationStatus.AUTHORIZED
    )

    readiness = service.assess(authorization)

    assert readiness.status == ExecutionReadinessStatus.READY
    assert (
        readiness.reason
        == "Execution authorization is present and the plan is ready."
    )


def test_unknown_authorization_produces_unknown_readiness():

    service = ExecutionReadinessService()

    authorization = build_authorization(
        ExecutionAuthorizationStatus.UNKNOWN
    )

    readiness = service.assess(authorization)

    assert readiness.status == ExecutionReadinessStatus.UNKNOWN
    assert (
        readiness.reason
        == "Execution readiness could not be determined."
    )