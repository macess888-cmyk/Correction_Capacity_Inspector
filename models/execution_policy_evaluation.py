from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_policy_status import ExecutionPolicyStatus


@dataclass(frozen=True)
class ExecutionPolicyEvaluation:
    execution_policy_evaluation_id: str
    execution_policy_id: str
    execution_intent_id: str
    status: ExecutionPolicyStatus
    evaluated_at: datetime
    reason: str
    evidence: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_policy_evaluation_id",
            self.execution_policy_evaluation_id,
        )
        self._validate_required_text(
            "execution_policy_id",
            self.execution_policy_id,
        )
        self._validate_required_text(
            "execution_intent_id",
            self.execution_intent_id,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if not isinstance(self.status, ExecutionPolicyStatus):
            raise TypeError(
                "status must be an ExecutionPolicyStatus"
            )

        if self.evaluated_at is None:
            raise ValueError("evaluated_at must not be None")

        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("evaluated_at must be a datetime")

        if not isinstance(self.evidence, Mapping):
            raise TypeError("evidence must be a mapping")

        object.__setattr__(
            self,
            "evidence",
            MappingProxyType(dict(self.evidence)),
        )

    @staticmethod
    def _validate_required_text(
        field_name: str,
        value: str,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string"
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} must not be empty"
            )