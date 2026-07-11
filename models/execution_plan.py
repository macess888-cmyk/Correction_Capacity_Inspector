from __future__ import annotations

from dataclasses import dataclass, field

from models.execution_plan_status import ExecutionPlanStatus
from models.execution_plan_step import ExecutionPlanStep
from models.execution_recommendation import ExecutionRecommendation


@dataclass(frozen=True)
class ExecutionPlan:
    """
    Organizes an execution recommendation into an ordered
    advisory plan.

    A plan grants no authority, performs no mutation,
    and executes no correction.
    """

    execution_id: str

    recommendation: ExecutionRecommendation

    status: ExecutionPlanStatus

    steps: tuple[ExecutionPlanStep, ...] = field(default_factory=tuple)