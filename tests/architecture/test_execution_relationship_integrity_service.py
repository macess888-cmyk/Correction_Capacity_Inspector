from datetime import datetime, timezone

from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_envelope import ExecutionEnvelope
from models.execution_envelope_status import ExecutionEnvelopeStatus
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
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)
from services.execution_relationship_integrity_service import (
    ExecutionRelationshipIntegrityService,
)


def build_envelope(
    *,
    envelope_execution_id: str = "exec-001",
    readiness_execution_id: str = "exec-001",
    authorization_execution_id: str = "exec-001",
    plan_execution_id: str = "exec-001",
    recommendation_execution_id: str = "exec-001",
) -> ExecutionEnvelope:

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
        execution_id=recommendation_execution_id,
        inspection=inspection,
        status=ExecutionRecommendationStatus.AVAILABLE,
        recommendation_type=ExecutionRecommendationType.VERIFY_RUNTIME,
        reason="Verify runtime.",
    )

    plan = ExecutionPlan(
        execution_id=plan_execution_id,
        recommendation=recommendation,
        status=ExecutionPlanStatus.AVAILABLE,
    )

    authorization = ExecutionAuthorization(
        execution_id=authorization_execution_id,
        plan=plan,
        status=ExecutionAuthorizationStatus.AUTHORIZED,
        reason="Authorized.",
    )

    readiness = ExecutionReadiness(
        execution_id=readiness_execution_id,
        authorization=authorization,
        status=ExecutionReadinessStatus.READY,
        reason="Ready.",
    )

    return ExecutionEnvelope(
        execution_id=envelope_execution_id,
        readiness=readiness,
        status=ExecutionEnvelopeStatus.COMPLETE,
        created_at=datetime.now(timezone.utc),
    )


def test_matching_execution_chain_is_valid():

    service = ExecutionRelationshipIntegrityService()

    integrity = service.inspect(build_envelope())

    assert integrity.execution_id == "exec-001"
    assert (
        integrity.status
        == ExecutionRelationshipIntegrityStatus.VALID
    )
    assert integrity.observations == ()


def test_envelope_and_readiness_identity_mismatch_is_broken():

    service = ExecutionRelationshipIntegrityService()

    integrity = service.inspect(
        build_envelope(readiness_execution_id="exec-002")
    )

    assert (
        integrity.status
        == ExecutionRelationshipIntegrityStatus.BROKEN
    )
    assert integrity.observations == (
        "Envelope execution identity does not match readiness.",
    )


def test_readiness_and_authorization_identity_mismatch_is_broken():

    service = ExecutionRelationshipIntegrityService()

    integrity = service.inspect(
        build_envelope(authorization_execution_id="exec-002")
    )

    assert (
        integrity.status
        == ExecutionRelationshipIntegrityStatus.BROKEN
    )
    assert integrity.observations == (
        "Readiness execution identity does not match authorization.",
    )


def test_authorization_and_plan_identity_mismatch_is_broken():

    service = ExecutionRelationshipIntegrityService()

    integrity = service.inspect(
        build_envelope(plan_execution_id="exec-002")
    )

    assert (
        integrity.status
        == ExecutionRelationshipIntegrityStatus.BROKEN
    )
    assert integrity.observations == (
        "Authorization execution identity does not match plan.",
    )


def test_plan_and_recommendation_identity_mismatch_is_broken():

    service = ExecutionRelationshipIntegrityService()

    integrity = service.inspect(
        build_envelope(recommendation_execution_id="exec-002")
    )

    assert (
        integrity.status
        == ExecutionRelationshipIntegrityStatus.BROKEN
    )
    assert integrity.observations == (
        "Plan execution identity does not match recommendation.",
    )