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
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)


def build_consistent_inspection() -> ExecutionInspection:

    divergence = ExecutionDivergence(
        execution_id="exec-001",
        runtime_state="RUNNING",
        reconstructed_state="RUNNING",
        status=ExecutionDivergenceStatus.IDENTICAL,
    )

    return ExecutionInspection(
        execution_id="exec-001",
        divergence=divergence,
        status=ExecutionInspectionStatus.CONSISTENT,
        observations=(),
        requires_attention=False,
    )


def test_execution_recommendation_model():

    inspection = build_consistent_inspection()

    recommendation = ExecutionRecommendation(
        execution_id="exec-001",
        inspection=inspection,
        status=ExecutionRecommendationStatus.AVAILABLE,
        recommendation_type=ExecutionRecommendationType.NO_ACTION,
        reason="Execution is consistent with reconstructed history.",
    )

    assert recommendation.execution_id == "exec-001"
    assert recommendation.inspection == inspection
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


def test_execution_recommendation_is_frozen():

    inspection = build_consistent_inspection()

    recommendation = ExecutionRecommendation(
        execution_id="exec-001",
        inspection=inspection,
        status=ExecutionRecommendationStatus.AVAILABLE,
        recommendation_type=ExecutionRecommendationType.NO_ACTION,
        reason="Execution is consistent with reconstructed history.",
    )

    with pytest.raises(FrozenInstanceError):
        recommendation.execution_id = "changed"