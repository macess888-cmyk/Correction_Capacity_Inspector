from models.execution_divergence import ExecutionDivergence
from models.execution_divergence_status import (
    ExecutionDivergenceStatus,
)
from models.execution_inspection import ExecutionInspection
from models.execution_inspection_status import (
    ExecutionInspectionStatus,
)
from models.execution_plan_status import ExecutionPlanStatus
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)
from services.execution_plan_service import ExecutionPlanService


def build_recommendation(
    recommendation_type: ExecutionRecommendationType,
    status: ExecutionRecommendationStatus = (
        ExecutionRecommendationStatus.AVAILABLE
    ),
) -> ExecutionRecommendation:

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

    return ExecutionRecommendation(
        execution_id="exec-001",
        inspection=inspection,
        status=status,
        recommendation_type=recommendation_type,
        reason="Test recommendation.",
    )


def test_no_action_recommendation_produces_available_empty_plan():

    service = ExecutionPlanService()

    recommendation = build_recommendation(
        ExecutionRecommendationType.NO_ACTION
    )

    plan = service.plan(recommendation)

    assert plan.execution_id == "exec-001"
    assert plan.status == ExecutionPlanStatus.AVAILABLE
    assert plan.steps == ()


def test_verify_runtime_recommendation_produces_ordered_plan():

    service = ExecutionPlanService()

    recommendation = build_recommendation(
        ExecutionRecommendationType.VERIFY_RUNTIME
    )

    plan = service.plan(recommendation)

    assert plan.status == ExecutionPlanStatus.AVAILABLE
    assert len(plan.steps) == 3

    assert plan.steps[0].order == 1
    assert plan.steps[0].description == "Read the current runtime state."

    assert plan.steps[1].order == 2
    assert (
        plan.steps[1].description
        == "Compare runtime state with reconstructed history."
    )

    assert plan.steps[2].order == 3
    assert (
        plan.steps[2].description
        == "Record the runtime verification result."
    )


def test_continue_observation_recommendation_produces_observation_plan():

    service = ExecutionPlanService()

    recommendation = build_recommendation(
        ExecutionRecommendationType.CONTINUE_OBSERVATION
    )

    plan = service.plan(recommendation)

    assert plan.status == ExecutionPlanStatus.AVAILABLE
    assert len(plan.steps) == 2
    assert plan.steps[0].description == "Continue observing execution."
    assert (
        plan.steps[1].description
        == "Reinspect when runtime state becomes available."
    )


def test_request_evidence_recommendation_produces_incomplete_plan():

    service = ExecutionPlanService()

    recommendation = build_recommendation(
        ExecutionRecommendationType.REQUEST_EVIDENCE,
        status=ExecutionRecommendationStatus.INSUFFICIENT_INFORMATION,
    )

    plan = service.plan(recommendation)

    assert plan.status == ExecutionPlanStatus.INCOMPLETE
    assert len(plan.steps) == 2
    assert plan.steps[0].description == "Identify missing execution evidence."
    assert plan.steps[1].description == "Request the missing evidence."


def test_unknown_recommendation_is_not_plannable():

    service = ExecutionPlanService()

    recommendation = build_recommendation(
        ExecutionRecommendationType.UNKNOWN,
        status=ExecutionRecommendationStatus.UNKNOWN,
    )

    plan = service.plan(recommendation)

    assert plan.status == ExecutionPlanStatus.NOT_PLANNABLE
    assert plan.steps == ()