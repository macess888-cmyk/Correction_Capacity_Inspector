from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)


@dataclass(frozen=True)
class ExecutionRelianceDecision:
    execution_reliance_decision_id: str
    subject_id: str
    reliance_evaluation_id: str
    decision: ExecutionRelianceDecisionType
    decided_at: datetime
    decided_by: str
    reason: str
    conditions: Iterable[str]
    evidence_references: Iterable[str]
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_reliance_decision_id",
            self.execution_reliance_decision_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "reliance_evaluation_id",
            self.reliance_evaluation_id,
        )
        self._validate_required_text(
            "decided_by",
            self.decided_by,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if not isinstance(
            self.decision,
            ExecutionRelianceDecisionType,
        ):
            raise TypeError(
                "decision must be an ExecutionRelianceDecisionType"
            )

        if self.decided_at is None:
            raise ValueError("decided_at must not be None")

        if not isinstance(self.decided_at, datetime):
            raise TypeError("decided_at must be a datetime")

        conditions = tuple(self.conditions)

        for condition in conditions:
            self._validate_required_text(
                "condition",
                condition,
            )

        if (
            self.decision
            is ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT
            and not conditions
        ):
            raise ValueError(
                "conditional accept must contain conditions"
            )

        if (
            self.decision
            is not ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT
            and conditions
        ):
            raise ValueError(
                "non-conditional decision must not contain conditions"
            )

        references = tuple(self.evidence_references)

        for reference in references:
            self._validate_required_text(
                "evidence_reference",
                reference,
            )

        if self.subject_id not in references:
            raise ValueError(
                "evidence_references must include subject_id"
            )

        if self.reliance_evaluation_id not in references:
            raise ValueError(
                "evidence_references must include "
                "reliance_evaluation_id"
            )

        if len(references) != len(set(references)):
            raise ValueError(
                "evidence_references must not contain duplicates"
            )

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

        object.__setattr__(
            self,
            "conditions",
            conditions,
        )

        object.__setattr__(
            self,
            "evidence_references",
            references,
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
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