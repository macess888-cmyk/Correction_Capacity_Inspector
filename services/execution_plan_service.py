from models.execution_plan import ExecutionPlan
from models.execution_plan_status import ExecutionPlanStatus
from models.execution_plan_step import ExecutionPlanStep
from models.execution_recommendation import ExecutionRecommendation
from models.execution_recommendation_type import (
    ExecutionRecommendationType,
)


class ExecutionPlanService:
    """
    Organizes execution recommendations into advisory plans.

    Plans grant no authority, perform no mutation,
    and execute no correction.
    """

    def plan(
        self,
        recommendation: ExecutionRecommendation,
    ) -> ExecutionPlan:

        if (
            recommendation.recommendation_type
            == ExecutionRecommendationType.NO_ACTION
        ):
            return ExecutionPlan(
                execution_id=recommendation.execution_id,
                recommendation=recommendation,
                status=ExecutionPlanStatus.AVAILABLE,
                steps=(),
            )

        if (
            recommendation.recommendation_type
            == ExecutionRecommendationType.VERIFY_RUNTIME
        ):
            return ExecutionPlan(
                execution_id=recommendation.execution_id,
                recommendation=recommendation,
                status=ExecutionPlanStatus.AVAILABLE,
                steps=(
                    ExecutionPlanStep(
                        order=1,
                        description="Read the current runtime state.",
                    ),
                    ExecutionPlanStep(
                        order=2,
                        description=(
                            "Compare runtime state with reconstructed history."
                        ),
                    ),
                    ExecutionPlanStep(
                        order=3,
                        description=(
                            "Record the runtime verification result."
                        ),
                    ),
                ),
            )

        if (
            recommendation.recommendation_type
            == ExecutionRecommendationType.CONTINUE_OBSERVATION
        ):
            return ExecutionPlan(
                execution_id=recommendation.execution_id,
                recommendation=recommendation,
                status=ExecutionPlanStatus.AVAILABLE,
                steps=(
                    ExecutionPlanStep(
                        order=1,
                        description="Continue observing execution.",
                    ),
                    ExecutionPlanStep(
                        order=2,
                        description=(
                            "Reinspect when runtime state becomes available."
                        ),
                    ),
                ),
            )

        if (
            recommendation.recommendation_type
            == ExecutionRecommendationType.REQUEST_EVIDENCE
        ):
            return ExecutionPlan(
                execution_id=recommendation.execution_id,
                recommendation=recommendation,
                status=ExecutionPlanStatus.INCOMPLETE,
                steps=(
                    ExecutionPlanStep(
                        order=1,
                        description="Identify missing execution evidence.",
                    ),
                    ExecutionPlanStep(
                        order=2,
                        description="Request the missing evidence.",
                    ),
                ),
            )

        if (
            recommendation.recommendation_type
            == ExecutionRecommendationType.UNKNOWN
        ):
            return ExecutionPlan(
                execution_id=recommendation.execution_id,
                recommendation=recommendation,
                status=ExecutionPlanStatus.NOT_PLANNABLE,
                steps=(),
            )

        return ExecutionPlan(
            execution_id=recommendation.execution_id,
            recommendation=recommendation,
            status=ExecutionPlanStatus.UNKNOWN,
            steps=(),
        )