from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from models.execution_attestation_status import (
    ExecutionAttestationStatus,
)


@dataclass(frozen=True)
class ExecutionAttestation:
    execution_attestation_id: str
    subject_id: str
    certification_id: str
    status: ExecutionAttestationStatus
    statement: str
    attested_at: datetime
    attested_by: str
    evidence_references: Iterable[str]
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_attestation_id",
            self.execution_attestation_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "certification_id",
            self.certification_id,
        )
        self._validate_required_text(
            "statement",
            self.statement,
        )
        self._validate_required_text(
            "attested_by",
            self.attested_by,
        )

        if not isinstance(
            self.status,
            ExecutionAttestationStatus,
        ):
            raise TypeError(
                "status must be an ExecutionAttestationStatus"
            )

        if self.attested_at is None:
            raise ValueError("attested_at must not be None")

        if not isinstance(self.attested_at, datetime):
            raise TypeError("attested_at must be a datetime")

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