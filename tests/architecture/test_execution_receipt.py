from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_admissibility import ExecutionAdmissibility
from models.execution_admissibility_status import (
    ExecutionAdmissibilityStatus,
)
from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_context_integrity import ExecutionContextIntegrity
from models.execution_context_integrity_status import (
    ExecutionContextIntegrityStatus,
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
from models.execution_receipt import ExecutionReceipt
from models.execution_receipt_status import ExecutionReceiptStatus
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)
from models.execution_refusal import ExecutionRefusal
from models.execution_refusal_status import ExecutionRefusalStatus
from models.execution_refusal_type import ExecutionRefusalType
from models.execution_relationship_integrity import (
    ExecutionRelationshipIntegrity,
)
from models.execution_relationship_integrity_status import (
    ExecutionRelationshipIntegrityStatus,
)
from models.execution_temporal_integrity import ExecutionTemporalIntegrity
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)


def build_admissibility() -> ExecutionAdmissibility:

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

    now = datetime.now(timezone.utc)

    envelope = ExecutionEnvelope(
        execution_id="exec-001",
        readiness=readiness,
        status=ExecutionEnvelopeStatus.COMPLETE,
        created_at=now,
    )

    relationship_integrity = ExecutionRelationshipIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=ExecutionRelationshipIntegrityStatus.VALID,
    )

    temporal_integrity = ExecutionTemporalIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=ExecutionTemporalIntegrityStatus.CURRENT,
        inspected_at=now,
    )

    context_integrity = ExecutionContextIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        expected_context={"environment": "production"},
        observed_context={"environment": "production"},
        status=ExecutionContextIntegrityStatus.CORRESPONDING,
    )

    refusal = ExecutionRefusal(
        execution_id="exec-001",
        envelope=envelope,
        relationship_integrity=relationship_integrity,
        temporal_integrity=temporal_integrity,
        status=ExecutionRefusalStatus.NOT_REFUSED,
        refusal_type=ExecutionRefusalType.UNKNOWN,
        reason="No refusal condition was established.",
    )

    return ExecutionAdmissibility(
        execution_id="exec-001",
        envelope=envelope,
        relationship_integrity=relationship_integrity,
        temporal_integrity=temporal_integrity,
        context_integrity=context_integrity,
        refusal=refusal,
        status=ExecutionAdmissibilityStatus.ADMISSIBLE,
        reason="All execution governance conditions are satisfied.",
    )


def test_execution_receipt_model():

    admissibility = build_admissibility()

    recorded_at = datetime.now(timezone.utc)

    receipt = ExecutionReceipt(
        execution_id="exec-001",
        admissibility=admissibility,
        status=ExecutionReceiptStatus.COMPLETED,
        recorded_at=recorded_at,
        operation="VERIFY_RUNTIME",
        outcome="Runtime verification completed.",
    )

    assert receipt.execution_id == "exec-001"
    assert receipt.admissibility == admissibility
    assert receipt.status == ExecutionReceiptStatus.COMPLETED
    assert receipt.recorded_at == recorded_at
    assert receipt.operation == "VERIFY_RUNTIME"
    assert receipt.outcome == "Runtime verification completed."
    assert receipt.observations == ()


def test_execution_receipt_is_frozen():

    admissibility = build_admissibility()

    receipt = ExecutionReceipt(
        execution_id="exec-001",
        admissibility=admissibility,
        status=ExecutionReceiptStatus.NOT_ATTEMPTED,
        recorded_at=datetime.now(timezone.utc),
        operation="VERIFY_RUNTIME",
        outcome="Execution was not attempted.",
    )

    with pytest.raises(FrozenInstanceError):
        receipt.execution_id = "changed"