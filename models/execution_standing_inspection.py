from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_standing_status import ExecutionStandingStatus


@dataclass(frozen=True)
class ExecutionStandingInspection:
    execution_standing_inspection_id: str
    subject_id: str
    subject_type: str
    status: ExecutionStandingStatus
    inspected_at: datetime
    reason: str
    governing_record_id: str
    evidence_references: Iterable[str]
    findings: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_standing_inspection_id",
            self.execution_standing_inspection_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "subject_type",
            self.subject_type,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )
        self._validate_required_text(
            "governing_record_id",
            self.governing_record_id,
        )

        if not isinstance(self.status, ExecutionStandingStatus):
            raise TypeError(
                "status must be an ExecutionStandingStatus"
            )

        if self.inspected_at is None:
            raise ValueError("inspected_at must not be None")

        if not isinstance(self.inspected_at, datetime):
            raise TypeError("inspected_at must be a datetime")

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

        if self.governing_record_id not in references:
            raise ValueError(
                "evidence_references must include governing_record_id"
            )

        if len(references) != len(set(references)):
            raise ValueError(
                "evidence_references must not contain duplicates"
            )

        if not isinstance(self.findings, Mapping):
            raise TypeError("findings must be a mapping")

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