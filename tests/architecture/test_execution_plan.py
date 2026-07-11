from dataclasses import FrozenInstanceError

import pytest

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
from models.execution_plan_step import ExecutionPlanStep
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)


def build_recommendation() -> ExecutionRecommendation:

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
        observations=(
            "Runtime state differs from reconstructed execution state.",
        ),
        requires_attention=True,
    )

    return ExecutionRecommendation(
        execution_id="exec-001",
        inspection=inspection,
        status=ExecutionRecommendationStatus.AVAILABLE,
        recommendation_type=ExecutionRecommendationType.VERIFY_RUNTIME,
        reason=(
            "Runtime state should be verified against "
            "reconstructed history."
        ),
    )


def test_execution_plan_model():

    recommendation = build_recommendation()

    steps = (
        ExecutionPlanStep(
            order=1,
            description="Read the current runtime state.",
        ),
        ExecutionPlanStep(
            order=2,
            description="Compare runtime state with reconstructed history.",
        ),
    )

    plan = ExecutionPlan(
        execution_id="exec-001",
        recommendation=recommendation,
        status=ExecutionPlanStatus.AVAILABLE,
        steps=steps,
    )

    assert plan.execution_id == "exec-001"
    assert plan.recommendation == recommendation
    assert plan.status == ExecutionPlanStatus.AVAILABLE
    assert plan.steps == steps


def test_execution_plan_step_defaults():

    step = ExecutionPlanStep(
        order=1,
        description="Continue observing execution.",
    )

    assert step.order == 1
    assert step.description == "Continue observing execution."
    assert step.required is True


def test_execution_plan_is_frozen():

    recommendation = build_recommendation()

    plan = ExecutionPlan(
        execution_id="exec-001",
        recommendation=recommendation,
        status=ExecutionPlanStatus.AVAILABLE,
    )

    with pytest.raises(FrozenInstanceError):
        plan.execution_id = "changed"


def test_execution_plan_step_is_frozen():

    step = ExecutionPlanStep(
        order=1,
        description="Verify runtime state.",
    )

    with pytest.raises(FrozenInstanceError):
        step.order = 2