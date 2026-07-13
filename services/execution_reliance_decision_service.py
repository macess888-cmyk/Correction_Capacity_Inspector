from __future__ import annotations

from datetime import datetime

from models.execution_reliance_decision import (
    ExecutionRelianceDecision,
)
from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)
from models.execution_reliance_evaluation import (
    ExecutionRelianceEvaluation,
)
from models.execution_reliance_status import ExecutionRelianceStatus


class ExecutionRelianceDecisionService:
    """Creates governance decisions from reliance evaluations."""

    def decide(
        self,
        *,
        execution_reliance_decision_id: str,
        evaluation: ExecutionRelianceEvaluation,
        decided_at: datetime,
        decided_by: str,
    ) -> ExecutionRelianceDecision:
        if not isinstance(
            evaluation,
            ExecutionRelianceEvaluation,
        ):
            raise TypeError(
                "evaluation must be an "
                "ExecutionRelianceEvaluation"
            )

        decision, reason, conditions = self._map_evaluation(
            evaluation
        )

        references = self._build_evidence_references(
            evaluation
        )

        return ExecutionRelianceDecision(
            execution_reliance_decision_id=(
                execution_reliance_decision_id
            ),
            subject_id=evaluation.subject_id,
            reliance_evaluation_id=(
                evaluation.execution_reliance_evaluation_id
            ),
            decision=decision,
            decided_at=decided_at,
            decided_by=decided_by,
            reason=reason,
            conditions=conditions,
            evidence_references=references,
            metadata={
                "reliance_status": evaluation.status.value,
            },
        )

    @staticmethod
    def _map_evaluation(
        evaluation: ExecutionRelianceEvaluation,
    ) -> tuple[
        ExecutionRelianceDecisionType,
        str,
        tuple[str, ...],
    ]:
        if evaluation.status is ExecutionRelianceStatus.RELIABLE:
            return (
                ExecutionRelianceDecisionType.ACCEPT,
                "current reliance is supported",
                (),
            )

        if (
            evaluation.status
            is ExecutionRelianceStatus.NOT_RELIABLE
        ):
            return (
                ExecutionRelianceDecisionType.REJECT,
                "current reliance is not supported",
                (),
            )

        if (
            evaluation.status
            is ExecutionRelianceStatus.CONDITIONALLY_RELIABLE
        ):
            return (
                ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT,
                "current reliance is accepted subject to conditions",
                evaluation.conditions,
            )

        return (
            ExecutionRelianceDecisionType.HOLD,
            "current reliance is indeterminate",
            (),
        )

    @staticmethod
    def _build_evidence_references(
        evaluation: ExecutionRelianceEvaluation,
    ) -> tuple[str, ...]:
        references: list[str] = [
            evaluation.subject_id,
            evaluation.execution_reliance_evaluation_id,
        ]

        for reference in evaluation.evidence_references:
            if reference not in references:
                references.append(reference)

        return tuple(references)