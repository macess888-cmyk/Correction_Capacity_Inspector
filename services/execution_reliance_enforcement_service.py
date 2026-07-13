from __future__ import annotations

from datetime import datetime

from models.execution_reliance_decision import (
    ExecutionRelianceDecision,
)
from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)
from models.execution_reliance_enforcement import (
    ExecutionRelianceEnforcement,
)
from models.execution_reliance_enforcement_outcome import (
    ExecutionRelianceEnforcementOutcome,
)


class ExecutionRelianceEnforcementService:
    """Applies an explicit reliance decision to present use."""

    def enforce(
        self,
        *,
        execution_reliance_enforcement_id: str,
        decision: ExecutionRelianceDecision,
        enforced_at: datetime,
        enforced_by: str,
    ) -> ExecutionRelianceEnforcement:
        if not isinstance(decision, ExecutionRelianceDecision):
            raise TypeError(
                "decision must be an ExecutionRelianceDecision"
            )

        outcome, reason, conditions = self._map_decision(
            decision
        )

        references = self._build_evidence_references(
            decision
        )

        return ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id=(
                execution_reliance_enforcement_id
            ),
            subject_id=decision.subject_id,
            reliance_decision_id=(
                decision.execution_reliance_decision_id
            ),
            outcome=outcome,
            enforced_at=enforced_at,
            enforced_by=enforced_by,
            reason=reason,
            conditions=conditions,
            evidence_references=references,
            metadata={
                "reliance_decision": decision.decision.value,
                "scope": "present-use",
            },
        )

    @staticmethod
    def _map_decision(
        decision: ExecutionRelianceDecision,
    ) -> tuple[
        ExecutionRelianceEnforcementOutcome,
        str,
        tuple[str, ...],
    ]:
        if decision.decision is ExecutionRelianceDecisionType.ACCEPT:
            return (
                ExecutionRelianceEnforcementOutcome.PERMITTED,
                "reliance decision permits present use",
                (),
            )

        if decision.decision is ExecutionRelianceDecisionType.REJECT:
            return (
                ExecutionRelianceEnforcementOutcome.BLOCKED,
                "reliance decision blocks present use",
                (),
            )

        if decision.decision is ExecutionRelianceDecisionType.HOLD:
            return (
                ExecutionRelianceEnforcementOutcome.HELD,
                "reliance decision places present use on hold",
                (),
            )

        return (
            ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED,
            "present use is permitted subject to conditions",
            decision.conditions,
        )

    @staticmethod
    def _build_evidence_references(
        decision: ExecutionRelianceDecision,
    ) -> tuple[str, ...]:
        references: list[str] = [
            decision.subject_id,
            decision.execution_reliance_decision_id,
        ]

        for reference in decision.evidence_references:
            if reference not in references:
                references.append(reference)

        return tuple(references)