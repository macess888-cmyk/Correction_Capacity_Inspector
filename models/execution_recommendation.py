from __future__ import annotations

from dataclasses import dataclass

from models.execution_inspection import ExecutionInspection
from models.execution_recommendation_status import (
    ExecutionRecommendationStatus,
)
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)


@dataclass(frozen=True)
class ExecutionRecommendation:
    """
    Represents a candidate response derived from execution inspection.

    A recommendation is advisory only.

    It carries no authority, grants no permission,
    performs no mutation, and executes no correction.
    """

    execution_id: str

    inspection: ExecutionInspection

    status: ExecutionRecommendationStatus

    recommendation_type: ExecutionRecommendationType

    reason: str