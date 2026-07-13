from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_reliance_enforcement_outcome import (
    ExecutionRelianceEnforcementOutcome,
)


@dataclass(frozen=True)
class ExecutionRelianceEnforcement:
    execution_reliance_enforcement_id: str
    subject_id: str
    reliance_decision_id: str
    outcome: ExecutionRelianceEnforcementOutcome
    enforced_at: datetime
    enforced_by: str
    reason: str
    conditions: Iterable[str]
    evidence_references: Iterable[str]
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_reliance_enforcement_id",
            self.execution_reliance_enforcement_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "reliance_decision_id",
            self.reliance_decision_id,
        )
        self._validate_required_text(
            "enforced_by",
            self.enforced_by,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if not isinstance(
            self.outcome,
            ExecutionRelianceEnforcementOutcome,
        ):
            raise TypeError(
                "outcome must be an "
                "ExecutionRelianceEnforcementOutcome"
            )

        if self.enforced_at is None:
            raise ValueError("enforced_at must not be None")

        if not isinstance(self.enforced_at, datetime):
            raise TypeError("enforced_at must be a datetime")

        conditions = tuple(self.conditions)

        for condition in conditions:
            self._validate_required_text(
                "condition",
                condition,
            )

        if (
            self.outcome
            is ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED
            and not conditions
        ):
            raise ValueError(
                "conditionally permitted enforcement "
                "must contain conditions"
            )

        if (
            self.outcome
            is not ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED
            and conditions
        ):
            raise ValueError(
                "non-conditional enforcement must not "
                "contain conditions"
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

        if self.reliance_decision_id not in references:
            raise ValueError(
                "evidence_references must include reliance_decision_id"
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