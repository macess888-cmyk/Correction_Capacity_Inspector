from datetime import datetime, timedelta, timezone

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
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)
from services.execution_temporal_integrity_service import (
    ExecutionTemporalIntegrityService,
)


def build_envelope(
    *,
    created_at: datetime,
    expires_at: datetime | None,
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

    readiness = ExecutionReadiness(
        execution_id="exec-001",
        authorization=authorization,
        status=ExecutionReadinessStatus.READY,
        reason="Ready.",
    )

    return ExecutionEnvelope(
        execution_id="exec-001",
        readiness=readiness,
        status=ExecutionEnvelopeStatus.COMPLETE,
        created_at=created_at,
        expires_at=expires_at,
    )


def test_unexpired_envelope_is_current():

    service = ExecutionTemporalIntegrityService()

    created_at = datetime(
        2026,
        7,
        11,
        12,
        0,
        tzinfo=timezone.utc,
    )

    envelope = build_envelope(
        created_at=created_at,
        expires_at=created_at + timedelta(minutes=30),
    )

    integrity = service.inspect(
        envelope,
        inspected_at=created_at + timedelta(minutes=10),
    )

    assert integrity.execution_id == "exec-001"
    assert (
        integrity.status
        == ExecutionTemporalIntegrityStatus.CURRENT
    )
    assert integrity.observations == ()


def test_expired_envelope_is_expired():

    service = ExecutionTemporalIntegrityService()

    created_at = datetime(
        2026,
        7,
        11,
        12,
        0,
        tzinfo=timezone.utc,
    )

    envelope = build_envelope(
        created_at=created_at,
        expires_at=created_at + timedelta(minutes=30),
    )

    integrity = service.inspect(
        envelope,
        inspected_at=created_at + timedelta(minutes=31),
    )

    assert (
        integrity.status
        == ExecutionTemporalIntegrityStatus.EXPIRED
    )
    assert integrity.observations == (
        "Execution envelope has expired.",
    )


def test_envelope_without_expiry_is_current():

    service = ExecutionTemporalIntegrityService()

    created_at = datetime(
        2026,
        7,
        11,
        12,
        0,
        tzinfo=timezone.utc,
    )

    envelope = build_envelope(
        created_at=created_at,
        expires_at=None,
    )

    integrity = service.inspect(
        envelope,
        inspected_at=created_at + timedelta(hours=1),
    )

    assert (
        integrity.status
        == ExecutionTemporalIntegrityStatus.CURRENT
    )
    assert integrity.observations == ()


def test_inspection_before_envelope_creation_is_unknown():

    service = ExecutionTemporalIntegrityService()

    created_at = datetime(
        2026,
        7,
        11,
        12,
        0,
        tzinfo=timezone.utc,
    )

    envelope = build_envelope(
        created_at=created_at,
        expires_at=created_at + timedelta(minutes=30),
    )

    integrity = service.inspect(
        envelope,
        inspected_at=created_at - timedelta(minutes=1),
    )

    assert (
        integrity.status
        == ExecutionTemporalIntegrityStatus.UNKNOWN
    )
    assert integrity.observations == (
        "Execution envelope was inspected before its creation time.",
    )