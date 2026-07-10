from __future__ import annotations

from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)
from registries.correction_capacity_assessment_registry import (
    CorrectionCapacityAssessmentRegistry,
)


class CorrectionCapacityAssessmentService:
    """
    Service responsible for assessment lifecycle operations.

    This service performs no scoring, inference,
    decision-making, or execution.
    """

    def __init__(
        self,
        registry: CorrectionCapacityAssessmentRegistry,
    ) -> None:
        self._registry = registry

    def create_assessment(
        self,
        assessment: CorrectionCapacityAssessment,
    ) -> None:
        self._registry.add(assessment)

    def get_assessment(
        self,
        assessment_id: str,
    ) -> CorrectionCapacityAssessment:
        return self._registry.get(assessment_id)

    def update_assessment(
        self,
        assessment: CorrectionCapacityAssessment,
    ) -> None:
        self._registry.update(assessment)

    def complete_assessment(
        self,
        assessment_id: str,
    ) -> CorrectionCapacityAssessment:
        assessment = self._registry.get(assessment_id)
        assessment.status = "COMPLETED"
        self._registry.update(assessment)
        return assessment

    def archive_assessment(
        self,
        assessment_id: str,
    ) -> CorrectionCapacityAssessment:
        assessment = self._registry.get(assessment_id)
        assessment.status = "ARCHIVED"
        self._registry.update(assessment)
        return assessment

    def list_assessments(
        self,
    ) -> list[CorrectionCapacityAssessment]:
        return self._registry.list()

    def assessment_exists(
        self,
        assessment_id: str,
    ) -> bool:
        return self._registry.exists(assessment_id)

    def count_assessments(self) -> int:
        return self._registry.count()