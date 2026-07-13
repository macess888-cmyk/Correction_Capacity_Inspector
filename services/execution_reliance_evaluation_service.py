from __future__ import annotations

from datetime import datetime

from models.execution_reliance_evaluation import (
    ExecutionRelianceEvaluation,
)
from models.execution_reliance_status import ExecutionRelianceStatus
from models.execution_standing_inspection import (
    ExecutionStandingInspection,
)
from models.execution_standing_status import ExecutionStandingStatus


class ExecutionRelianceEvaluationService:
    """Evaluates present reliance from an immutable standing inspection."""

    def evaluate(
        self,
        *,
        execution_reliance_evaluation_id: str,
        standing_inspection: ExecutionStandingInspection,
        evaluated_at: datetime,
    ) -> ExecutionRelianceEvaluation:
        if not isinstance(
            standing_inspection,
            ExecutionStandingInspection,
        ):
            raise TypeError(
                "standing_inspection must be an "
                "ExecutionStandingInspection"
            )

        status, reason, conditions = self._map_standing(
            standing_inspection.status
        )

        references = self._build_evidence_references(
            standing_inspection
        )

        return ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id=(
                execution_reliance_evaluation_id
            ),
            subject_id=standing_inspection.subject_id,
            standing_inspection_id=(
                standing_inspection.execution_standing_inspection_id
            ),
            status=status,
            evaluated_at=evaluated_at,
            reason=reason,
            conditions=conditions,
            evidence_references=references,
            findings={
                "standing_status": standing_inspection.status.value,
                "governing_record_id": (
                    standing_inspection.governing_record_id
                ),
            },
        )

    @staticmethod
    def _map_standing(
        status: ExecutionStandingStatus,
    ) -> tuple[
        ExecutionRelianceStatus,
        str,
        tuple[str, ...],
    ]:
        if status is ExecutionStandingStatus.ACTIVE:
            return (
                ExecutionRelianceStatus.RELIABLE,
                "subject standing is active",
                (),
            )

        if status in {
            ExecutionStandingStatus.REVOKED,
            ExecutionStandingStatus.WITHDRAWN,
        }:
            return (
                ExecutionRelianceStatus.NOT_RELIABLE,
                "subject standing does not support present reliance",
                (),
            )

        if status is ExecutionStandingStatus.SUSPENDED:
            return (
                ExecutionRelianceStatus.CONDITIONALLY_RELIABLE,
                "subject standing is suspended",
                (
                    "current standing is suspended",
                    "manual review is required before reliance",
                ),
            )

        return (
            ExecutionRelianceStatus.INDETERMINATE,
            "current reliance cannot be determined from standing",
            (),
        )

    @staticmethod
    def _build_evidence_references(
        standing_inspection: ExecutionStandingInspection,
    ) -> tuple[str, ...]:
        references: list[str] = [
            standing_inspection.subject_id,
            standing_inspection.execution_standing_inspection_id,
        ]

        for reference in standing_inspection.evidence_references:
            if reference not in references:
                references.append(reference)

        return tuple(references)