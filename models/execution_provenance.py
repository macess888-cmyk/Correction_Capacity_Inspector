from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_provenance_relationship import (
    ExecutionProvenanceRelationship,
)


@dataclass(frozen=True)
class ExecutionProvenance:
    execution_provenance_id: str
    subject_id: str
    source_id: str
    relationship: ExecutionProvenanceRelationship
    recorded_at: datetime
    recorded_by: str
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_provenance_id",
            self.execution_provenance_id,
        )
        self._validate_required_text(
            "subject_id",
            self.subject_id,
        )
        self._validate_required_text(
            "source_id",
            self.source_id,
        )
        self._validate_required_text(
            "recorded_by",
            self.recorded_by,
        )

        if self.subject_id == self.source_id:
            raise ValueError(
                "subject_id must not equal source_id"
            )

        if not isinstance(
            self.relationship,
            ExecutionProvenanceRelationship,
        ):
            raise TypeError(
                "relationship must be an "
                "ExecutionProvenanceRelationship"
            )

        if self.recorded_at is None:
            raise ValueError("recorded_at must not be None")

        if not isinstance(self.recorded_at, datetime):
            raise TypeError("recorded_at must be a datetime")

        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")

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