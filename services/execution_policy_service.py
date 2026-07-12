from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime
from typing import Any

from models.execution_intent import ExecutionIntent
from models.execution_policy_evaluation import ExecutionPolicyEvaluation
from models.execution_policy_status import ExecutionPolicyStatus


PolicyEvaluation = tuple[
    ExecutionPolicyStatus,
    str,
    Mapping[str, Any],
]

PolicyEvaluator = Callable[
    [ExecutionIntent],
    PolicyEvaluation,
]


class ExecutionPolicyService:
    """Evaluates execution intents against registered policies."""

    def __init__(self) -> None:
        self._policies: dict[str, PolicyEvaluator] = {}

    def register_policy(
        self,
        *,
        execution_policy_id: str,
        evaluator: PolicyEvaluator,
    ) -> None:
        if not isinstance(execution_policy_id, str):
            raise TypeError(
                "execution_policy_id must be a string"
            )

        if not execution_policy_id.strip():
            raise ValueError(
                "execution_policy_id must not be empty"
            )

        if not callable(evaluator):
            raise TypeError("evaluator must be callable")

        if execution_policy_id in self._policies:
            raise ValueError(
                "execution_policy_id is already registered"
            )

        self._policies[execution_policy_id] = evaluator

    def evaluate(
        self,
        *,
        execution_policy_evaluation_id: str,
        execution_policy_id: str,
        intent: ExecutionIntent,
        evaluated_at: datetime,
    ) -> ExecutionPolicyEvaluation:
        if not isinstance(intent, ExecutionIntent):
            raise TypeError(
                "intent must be an ExecutionIntent"
            )

        evaluator = self._policies.get(execution_policy_id)

        if evaluator is None:
            raise ValueError(
                f"no policy registered for: {execution_policy_id}"
            )

        status, reason, evidence = evaluator(intent)

        if not isinstance(status, ExecutionPolicyStatus):
            raise TypeError(
                "policy evaluator status must be an "
                "ExecutionPolicyStatus"
            )

        if not isinstance(reason, str):
            raise TypeError(
                "policy evaluator reason must be a string"
            )

        if not reason.strip():
            raise ValueError(
                "policy evaluator reason must not be empty"
            )

        if not isinstance(evidence, Mapping):
            raise TypeError(
                "policy evaluator evidence must be a mapping"
            )

        return ExecutionPolicyEvaluation(
            execution_policy_evaluation_id=(
                execution_policy_evaluation_id
            ),
            execution_policy_id=execution_policy_id,
            execution_intent_id=intent.execution_intent_id,
            status=status,
            evaluated_at=evaluated_at,
            reason=reason,
            evidence=evidence,
        )