from __future__ import annotations

from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)


class CorrectionCapacityAssessmentRegistry:
    """
    Mutable registry for CorrectionCapacityAssessment objects.

    Registry invariants:
    - Assessment identifiers must be unique.
    - Duplicate additions raise ValueError.
    - Missing reads, updates, and removals raise KeyError.
    """

    def __init__(self) -> None:
        self._assessments: dict[
            str,
            CorrectionCapacityAssessment,
        ] = {}

    def add(
        self,
        assessment: CorrectionCapacityAssessment,
    ) -> None:
        assessment_id = assessment.assessment_id

        if assessment_id in self._assessments:
            raise ValueError(
                "Correction capacity assessment already exists: "
                f"{assessment_id}"
            )

        self._assessments[assessment_id] = assessment

    def get(
        self,
        assessment_id: str,
    ) -> CorrectionCapacityAssessment:
        if assessment_id not in self._assessments:
            raise KeyError(
                "Correction capacity assessment not found: "
                f"{assessment_id}"
            )

        return self._assessments[assessment_id]

    def update(
        self,
        assessment: CorrectionCapacityAssessment,
    ) -> None:
        assessment_id = assessment.assessment_id

        if assessment_id not in self._assessments:
            raise KeyError(
                "Correction capacity assessment not found: "
                f"{assessment_id}"
            )

        self._assessments[assessment_id] = assessment

    def remove(
        self,
        assessment_id: str,
    ) -> CorrectionCapacityAssessment:
        if assessment_id not in self._assessments:
            raise KeyError(
                "Correction capacity assessment not found: "
                f"{assessment_id}"
            )

        return self._assessments.pop(assessment_id)

    def exists(
        self,
        assessment_id: str,
    ) -> bool:
        return assessment_id in self._assessments

    def list(
        self,
    ) -> list[CorrectionCapacityAssessment]:
        return list(self._assessments.values())

    def count(self) -> int:
        return len(self._assessments)