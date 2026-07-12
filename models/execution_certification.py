from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_certification_status import (
    ExecutionCertificationStatus,
)


@dataclass(frozen=True)
class ExecutionCertification:
    execution_certification_id: str
    certification_profile_id: str
    subject_id: str
    status: ExecutionCertificationStatus
    evaluated_at: datetime
    evaluated_by: str
    reason: str
    evidence_references: Iterable[str]
    findings: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_certification_id",
            self.execution_certification_id,
        )
        self._validate_required_text(
            "certification_profile_id",
            self.certification_profile_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "evaluated_by",
            self.evaluated_by,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if not isinstance(
            self.status,
            ExecutionCertificationStatus,
        ):
            raise TypeError(
                "status must be an ExecutionCertificationStatus"
            )

        if self.evaluated_at is None:
            raise ValueError("evaluated_at must not be None")

        if not isinstance(self.evaluated_at, datetime):
            raise TypeError("evaluated_at must be a datetime")

        references = tuple(self.evidence_references)

        for reference in references:
            self._validate_required_text(
                "evidence_reference",
                reference,
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