from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)
from services.execution_recommendation_service import (
    ExecutionRecommendationService,
)


def build_inspection(
    status: ExecutionInspectionStatus,
    requires_attention: bool,
) -> ExecutionInspection:

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    return ExecutionInspection(
        execution_id="exec-001",
        divergence=divergence,
        status=status,
        observations=(),
        requires_attention=requires_attention,
    )


def test_consistent_inspection_recommends_no_action():

    service = ExecutionRecommendationService()

    inspection = build_inspection(
        status=ExecutionInspectionStatus.CONSISTENT,
        requires_attention=False,
    )

    recommendation = service.recommend(inspection)

    assert recommendation.execution_id == "exec-001"
    assert (
        recommendation.status
        == ExecutionRecommendationStatus.AVAILABLE
    )
    assert (
        recommendation.recommendation_type
        == ExecutionRecommendationType.NO_ACTION
    )
    assert (
        recommendation.reason
        == "Execution is consistent with reconstructed history."
    )


def test_inconsistent_inspection_recommends_runtime_verification():

    service = ExecutionRecommendationService()

    inspection = build_inspection(
        status=ExecutionInspectionStatus.INCONSISTENT,
        requires_attention=True,
    )

    recommendation = service.recommend(inspection)

    assert (
        recommendation.status
        == ExecutionRecommendationStatus.AVAILABLE
    )
    assert (
        recommendation.recommendation_type
        == ExecutionRecommendationType.VERIFY_RUNTIME
    )
    assert (
        recommendation.reason
        == "Runtime state should be verified against reconstructed history."
    )


def test_partial_inspection_recommends_continued_observation():

    service = ExecutionRecommendationService()

    inspection = build_inspection(
        status=ExecutionInspectionStatus.PARTIAL,
        requires_attention=True,
    )

    recommendation = service.recommend(inspection)

    assert (
        recommendation.status
        == ExecutionRecommendationStatus.AVAILABLE
    )
    assert (
        recommendation.recommendation_type
        == ExecutionRecommendationType.CONTINUE_OBSERVATION
    )
    assert (
        recommendation.reason
        == "Continue observation until runtime state becomes available."
    )


def test_insufficient_evidence_recommends_requesting_evidence():

    service = ExecutionRecommendationService()

    inspection = build_inspection(
        status=ExecutionInspectionStatus.INSUFFICIENT_EVIDENCE,
        requires_attention=True,
    )

    recommendation = service.recommend(inspection)

    assert (
        recommendation.status
        == ExecutionRecommendationStatus.INSUFFICIENT_INFORMATION
    )
    assert (
        recommendation.recommendation_type
        == ExecutionRecommendationType.REQUEST_EVIDENCE
    )
    assert (
        recommendation.reason
        == "Additional execution evidence is required before further interpretation."
    )


def test_unknown_inspection_produces_unknown_recommendation():

    service = ExecutionRecommendationService()

    inspection = build_inspection(
        status=ExecutionInspectionStatus.UNKNOWN,
        requires_attention=True,
    )

    recommendation = service.recommend(inspection)

    assert recommendation.status == ExecutionRecommendationStatus.UNKNOWN
    assert (
        recommendation.recommendation_type
        == ExecutionRecommendationType.UNKNOWN
    )
    assert (
        recommendation.reason
        == "No recommendation could be derived from the execution inspection."
    )