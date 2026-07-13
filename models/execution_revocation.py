from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_revocation_status import (
    ExecutionRevocationStatus,
)


@dataclass(frozen=True)
class ExecutionRevocation:
    execution_revocation_id: str
    subject_id: str
    subject_type: str
    status: ExecutionRevocationStatus
    reason: str
    revoked_at: datetime
    revoked_by: str
    evidence_references: Iterable[str]
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_revocation_id",
            self.execution_revocation_id,
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
            "revoked_by",
            self.revoked_by,
        )

        if not isinstance(
            self.status,
            ExecutionRevocationStatus,
        ):
            raise TypeError(
                "status must be an ExecutionRevocationStatus"
            )

        if self.revoked_at is None:
            raise ValueError("revoked_at must not be None")

        if not isinstance(self.revoked_at, datetime):
            raise TypeError("revoked_at must be a datetime")

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

        if len(references) != len(set(references)):
            raise ValueError(
                "evidence_references must not contain duplicates"
            )

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

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