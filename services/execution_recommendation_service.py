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


class ExecutionRecommendationService:
    """
    Derives advisory recommendations from execution inspection.

    Recommendations carry no authority, grant no permission,
    perform no mutation, and execute no correction.
    """

    def recommend(
        self,
        inspection: ExecutionInspection,
    ) -> ExecutionRecommendation:

        if inspection.status == ExecutionInspectionStatus.CONSISTENT:
            return ExecutionRecommendation(
                execution_id=inspection.execution_id,
                inspection=inspection,
                status=ExecutionRecommendationStatus.AVAILABLE,
                recommendation_type=ExecutionRecommendationType.NO_ACTION,
                reason=(
                    "Execution is consistent with reconstructed history."
                ),
            )

        if inspection.status == ExecutionInspectionStatus.INCONSISTENT:
            return ExecutionRecommendation(
                execution_id=inspection.execution_id,
                inspection=inspection,
                status=ExecutionRecommendationStatus.AVAILABLE,
                recommendation_type=(
                    ExecutionRecommendationType.VERIFY_RUNTIME
                ),
                reason=(
                    "Runtime state should be verified against "
                    "reconstructed history."
                ),
            )

        if inspection.status == ExecutionInspectionStatus.PARTIAL:
            return ExecutionRecommendation(
                execution_id=inspection.execution_id,
                inspection=inspection,
                status=ExecutionRecommendationStatus.AVAILABLE,
                recommendation_type=(
                    ExecutionRecommendationType.CONTINUE_OBSERVATION
                ),
                reason=(
                    "Continue observation until runtime state "
                    "becomes available."
                ),
            )

        if (
            inspection.status
            == ExecutionInspectionStatus.INSUFFICIENT_EVIDENCE
        ):
            return ExecutionRecommendation(
                execution_id=inspection.execution_id,
                inspection=inspection,
                status=(
                    ExecutionRecommendationStatus.INSUFFICIENT_INFORMATION
                ),
                recommendation_type=(
                    ExecutionRecommendationType.REQUEST_EVIDENCE
                ),
                reason=(
                    "Additional execution evidence is required "
                    "before further interpretation."
                ),
            )

        return ExecutionRecommendation(
            execution_id=inspection.execution_id,
            inspection=inspection,
            status=ExecutionRecommendationStatus.UNKNOWN,
            recommendation_type=ExecutionRecommendationType.UNKNOWN,
            reason=(
                "No recommendation could be derived from "
                "the execution inspection."
            ),
        )