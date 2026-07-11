from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest

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
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)


def build_envelope() -> ExecutionEnvelope:

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

    created_at = datetime(
        2026,
        7,
        11,
        12,
        0,
        tzinfo=timezone.utc,
    )

    return ExecutionEnvelope(
        execution_id="exec-001",
        readiness=readiness,
        status=ExecutionEnvelopeStatus.COMPLETE,
        created_at=created_at,
        expires_at=created_at + timedelta(minutes=30),
    )


def test_execution_temporal_integrity_model():

    envelope = build_envelope()

    inspected_at = datetime(
        2026,
        7,
        11,
        12,
        10,
        tzinfo=timezone.utc,
    )

    integrity = ExecutionTemporalIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=ExecutionTemporalIntegrityStatus.CURRENT,
        inspected_at=inspected_at,
    )

    assert integrity.execution_id == "exec-001"
    assert integrity.envelope == envelope
    assert (
        integrity.status
        == ExecutionTemporalIntegrityStatus.CURRENT
    )
    assert integrity.inspected_at == inspected_at
    assert integrity.observations == ()


def test_execution_temporal_integrity_is_frozen():

    envelope = build_envelope()

    integrity = ExecutionTemporalIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=ExecutionTemporalIntegrityStatus.CURRENT,
        inspected_at=datetime.now(timezone.utc),
    )

    with pytest.raises(FrozenInstanceError):
        integrity.execution_id = "changed"