from datetime import datetime, timezone

from models.execution_admissibility_status import (
    ExecutionAdmissibilityStatus,
)
from models.execution_authorization import ExecutionAuthorization
from models.execution_authorization_status import (
    ExecutionAuthorizationStatus,
)
from models.execution_context_integrity import (
    ExecutionContextIntegrity,
)
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
from models.execution_temporal_integrity import (
    ExecutionTemporalIntegrity,
)
from models.execution_temporal_integrity_status import (
    ExecutionTemporalIntegrityStatus,
)
from services.execution_admissibility_service import (
    ExecutionAdmissibilityService,
)


def build_inputs(
    *,
    relationship_status: ExecutionRelationshipIntegrityStatus = (
        ExecutionRelationshipIntegrityStatus.VALID
    ),
    temporal_status: ExecutionTemporalIntegrityStatus = (
        ExecutionTemporalIntegrityStatus.CURRENT
    ),
    context_status: ExecutionContextIntegrityStatus = (
        ExecutionContextIntegrityStatus.CORRESPONDING
    ),
    refusal_status: ExecutionRefusalStatus = (
        ExecutionRefusalStatus.NOT_REFUSED
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
        status=relationship_status,
    )

    temporal_integrity = ExecutionTemporalIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        status=temporal_status,
        inspected_at=now,
    )

    context_integrity = ExecutionContextIntegrity(
        execution_id="exec-001",
        envelope=envelope,
        expected_context={"environment": "production"},
        observed_context={"environment": "production"},
        status=context_status,
    )

    refusal = ExecutionRefusal(
        execution_id="exec-001",
        envelope=envelope,
        relationship_integrity=relationship_integrity,
        temporal_integrity=temporal_integrity,
        status=refusal_status,
        refusal_type=ExecutionRefusalType.UNKNOWN,
        reason="Test refusal.",
    )

    return (
        envelope,
        relationship_integrity,
        temporal_integrity,
        context_integrity,
        refusal,
    )


def test_valid_governance_chain_is_admissible():

    service = ExecutionAdmissibilityService()

    result = service.assess(*build_inputs())

    assert result.execution_id == "exec-001"
    assert result.status == ExecutionAdmissibilityStatus.ADMISSIBLE
    assert (
        result.reason
        == "All execution governance conditions are satisfied."
    )


def test_refused_execution_is_not_admissible():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(refusal_status=ExecutionRefusalStatus.REFUSED)
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
    )
    assert result.reason == "Execution refusal has been established."


def test_indeterminate_refusal_produces_indeterminate_admissibility():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            refusal_status=ExecutionRefusalStatus.INDETERMINATE
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.INDETERMINATE
    )
    assert result.reason == "Execution refusal is indeterminate."


def test_broken_relationship_is_not_admissible():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            relationship_status=(
                ExecutionRelationshipIntegrityStatus.BROKEN
            )
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
    )
    assert result.reason == "Execution relationship integrity is not valid."


def test_expired_temporal_integrity_is_not_admissible():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            temporal_status=ExecutionTemporalIntegrityStatus.EXPIRED
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
    )
    assert result.reason == "Execution temporal integrity is not current."


def test_unknown_temporal_integrity_is_indeterminate():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            temporal_status=ExecutionTemporalIntegrityStatus.UNKNOWN
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.INDETERMINATE
    )
    assert (
        result.reason
        == "Execution temporal integrity could not be established."
    )


def test_drifted_context_is_not_admissible():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            context_status=ExecutionContextIntegrityStatus.DRIFTED
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.NOT_ADMISSIBLE
    )
    assert (
        result.reason
        == "Execution context integrity is not corresponding."
    )


def test_incomplete_context_is_indeterminate():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            context_status=ExecutionContextIntegrityStatus.INCOMPLETE
        )
    )

    assert (
        result.status
        == ExecutionAdmissibilityStatus.INDETERMINATE
    )
    assert (
        result.reason
        == "Execution context integrity is incomplete."
    )


def test_unknown_context_is_unknown():

    service = ExecutionAdmissibilityService()

    result = service.assess(
        *build_inputs(
            context_status=ExecutionContextIntegrityStatus.UNKNOWN
        )
    )

    assert result.status == ExecutionAdmissibilityStatus.UNKNOWN
    assert (
        result.reason
        == "Execution context integrity could not be established."
    )