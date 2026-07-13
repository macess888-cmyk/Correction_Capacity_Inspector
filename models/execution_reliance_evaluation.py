from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_reliance_status import ExecutionRelianceStatus


@dataclass(frozen=True)
class ExecutionRelianceEvaluation:
    execution_reliance_evaluation_id: str
    subject_id: str
    standing_inspection_id: str
    status: ExecutionRelianceStatus
    evaluated_at: datetime
    reason: str
    conditions: Iterable[str]
    evidence_references: Iterable[str]
    findings: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_reliance_evaluation_id",
            self.execution_reliance_evaluation_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "standing_inspection_id",
            self.standing_inspection_id,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if not isinstance(self.status, ExecutionRelianceStatus):
            raise TypeError(
                "status must be an ExecutionRelianceStatus"
            )

        if self.evaluated_at is None:
            raise ValueError("evaluated_at must not be None")

        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("evaluated_at must be a datetime")

        conditions = tuple(self.conditions)

        for condition in conditions:
            self._validate_required_text(
                "condition",
                condition,
            )

        if (
            self.status
            is ExecutionRelianceStatus.CONDITIONALLY_RELIABLE
            and not conditions
        ):
            raise ValueError(
                "conditionally reliable evaluation "
                "must contain conditions"
            )

        if (
            self.status
            is not ExecutionRelianceStatus.CONDITIONALLY_RELIABLE
            and conditions
        ):
            raise ValueError(
                "non-conditional evaluation must not "
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

        if self.standing_inspection_id not in references:
            raise ValueError(
                "evidence_references must include "
                "standing_inspection_id"
            )

        if len(references) != len(set(references)):
            raise ValueError(
                "evidence_references must not contain duplicates"
            )

        if not isinstance(self.findings, Mapping):
            raise TypeError("findings must be a mapping")

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
            "findings",
            MappingProxyType(dict(self.findings)),
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