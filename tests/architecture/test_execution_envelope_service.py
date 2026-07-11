from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_envelope_status import (
    ExecutionEnvelopeStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)
from models.execution_plan import ExecutionPlan
from models.execution_plan_status import ExecutionPlanStatus
from models.execution_readiness import ExecutionReadiness
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
from services.execution_envelope_service import (
    ExecutionEnvelopeService,
)


def build_readiness(
    status: ExecutionReadinessStatus,
) -> ExecutionReadiness:

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

    authorization = ExecutionAuthorization(
        execution_id="exec-001",
        plan=plan,
        status=ExecutionAuthorizationStatus.AUTHORIZED,
        reason="Authorized.",
    )

    return ExecutionReadiness(
        execution_id="exec-001",
        authorization=authorization,
        status=status,
        reason="Test readiness.",
    )


def test_ready_execution_produces_complete_envelope():

    service = ExecutionEnvelopeService()

    readiness = build_readiness(
        ExecutionReadinessStatus.READY
    )

    envelope = service.create(readiness)

    assert envelope.execution_id == "exec-001"
    assert envelope.status == ExecutionEnvelopeStatus.COMPLETE
    assert envelope.readiness == readiness
    assert envelope.expires_at is None


def test_not_ready_execution_produces_incomplete_envelope():

    service = ExecutionEnvelopeService()

    readiness = build_readiness(
        ExecutionReadinessStatus.NOT_READY
    )

    envelope = service.create(readiness)

    assert envelope.status == ExecutionEnvelopeStatus.INCOMPLETE


def test_blocked_execution_produces_invalid_envelope():

    service = ExecutionEnvelopeService()

    readiness = build_readiness(
        ExecutionReadinessStatus.BLOCKED
    )

    envelope = service.create(readiness)

    assert envelope.status == ExecutionEnvelopeStatus.INVALID


def test_unknown_readiness_produces_unknown_envelope():

    service = ExecutionEnvelopeService()

    readiness = build_readiness(
        ExecutionReadinessStatus.UNKNOWN
    )

    envelope = service.create(readiness)

    assert envelope.status == ExecutionEnvelopeStatus.UNKNOWN