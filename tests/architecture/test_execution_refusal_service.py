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
from models.execution_refusal_status import ExecutionRefusalStatus
from models.execution_refusal_type import ExecutionRefusalType
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)
from services.execution_refusal_service import ExecutionRefusalService


def build_inputs(
    *,
    envelope_status: ExecutionEnvelopeStatus = (
        ExecutionEnvelopeStatus.COMPLETE
    ),
    readiness_status: ExecutionReadinessStatus = (
        ExecutionReadinessStatus.READY
    ),
    authorization_status: ExecutionAuthorizationStatus = (
        ExecutionAuthorizationStatus.AUTHORIZED
    ),
    relationship_status: ExecutionRelationshipIntegrityStatus = (
        ExecutionRelationshipIntegrityStatus.VALID
    ),
    temporal_status: ExecutionTemporalIntegrityStatus = (
        ExecutionTemporalIntegrityStatus.CURRENT
    ),
):

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
        status=authorization_status,
        reason="Test authorization.",
    )

    readiness = ExecutionReadiness(
        execution_id="exec-001",
        authorization=authorization,
        status=readiness_status,
        reason="Test readiness.",
    )

    now = datetime.now(timezone.utc)

    envelope = ExecutionEnvelope(
        execution_id="exec-001",
        readiness=readiness,
        status=envelope_status,
        created_at=now,
    )

    relationship_integrity = ExecutionRelationshipIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=relationship_status,
    )

    temporal_integrity = ExecutionTemporalIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=temporal_status,
        inspected_at=now,
    )

    return envelope, relationship_integrity, temporal_integrity


def test_invalid_envelope_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        envelope_status=ExecutionEnvelopeStatus.INVALID
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert refusal.refusal_type == ExecutionRefusalType.ENVELOPE_INVALID
    assert refusal.reason == "Execution envelope is invalid."


def test_valid_current_ready_chain_is_not_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs()

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.NOT_REFUSED
    assert refusal.refusal_type == ExecutionRefusalType.UNKNOWN
    assert refusal.reason == "No refusal condition was established."


def test_incomplete_envelope_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        envelope_status=ExecutionEnvelopeStatus.INCOMPLETE
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert (
        refusal.refusal_type
        == ExecutionRefusalType.ENVELOPE_INCOMPLETE
    )
    assert refusal.reason == "Execution envelope is incomplete."


def test_broken_relationship_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        relationship_status=ExecutionRelationshipIntegrityStatus.BROKEN
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert (
        refusal.refusal_type
        == ExecutionRefusalType.RELATIONSHIP_BROKEN
    )
    assert refusal.reason == "Execution relationship integrity is broken."


def test_expired_temporal_integrity_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        temporal_status=ExecutionTemporalIntegrityStatus.EXPIRED
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert (
        refusal.refusal_type
        == ExecutionRefusalType.TEMPORALLY_EXPIRED
    )
    assert refusal.reason == "Execution envelope is temporally expired."


def test_unknown_temporal_integrity_is_indeterminate():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        temporal_status=ExecutionTemporalIntegrityStatus.UNKNOWN
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.INDETERMINATE
    assert (
        refusal.refusal_type
        == ExecutionRefusalType.TEMPORALLY_UNKNOWN
    )
    assert (
        refusal.reason
        == "Execution temporal integrity could not be established."
    )


def test_not_ready_execution_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        readiness_status=ExecutionReadinessStatus.NOT_READY
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert refusal.refusal_type == ExecutionRefusalType.NOT_READY
    assert refusal.reason == "Execution is not ready."


def test_not_authorized_execution_is_refused():

    service = ExecutionRefusalService()

    envelope, relationship_integrity, temporal_integrity = build_inputs(
        authorization_status=ExecutionAuthorizationStatus.NOT_AUTHORIZED
    )

    refusal = service.evaluate(
        envelope,
        relationship_integrity,
        temporal_integrity,
    )

    assert refusal.status == ExecutionRefusalStatus.REFUSED
    assert (
        refusal.refusal_type
        == ExecutionRefusalType.NOT_AUTHORIZED
    )
    assert refusal.reason == "Execution is not authorized."