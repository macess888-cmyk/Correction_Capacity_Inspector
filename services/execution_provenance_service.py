from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from models.execution_provenance import ExecutionProvenance
from models.execution_provenance_relationship import (
    ExecutionProvenanceRelationship,
)


class ExecutionProvenanceService:
    """Stores immutable execution provenance records."""

    def __init__(self) -> None:
        self._records: list[ExecutionProvenance] = []
        self._record_ids: set[str] = set()

    def record(
        self,
        *,
        execution_provenance_id: str,
        subject_id: str,
        source_id: str,
        relationship: ExecutionProvenanceRelationship,
        recorded_at: datetime,
        recorded_by: str,
        metadata: Mapping[str, Any],
    ) -> ExecutionProvenance:
        if execution_provenance_id in self._record_ids:
            raise ValueError(
                "execution_provenance_id must be unique"
            )

        provenance = ExecutionProvenance(
            execution_provenance_id=execution_provenance_id,
            subject_id=subject_id,
            source_id=source_id,
            relationship=relationship,
            recorded_at=recorded_at,
            recorded_by=recorded_by,
            metadata=metadata,
        )

        self._records.append(provenance)
        self._record_ids.add(execution_provenance_id)

        return provenance

    def records(self) -> tuple[ExecutionProvenance, ...]:
        return tuple(self._records)

    def records_for_subject(
        self,
        subject_id: str,
    ) -> tuple[ExecutionProvenance, ...]:
        self._validate_filter_text("subject_id", subject_id)

        return tuple(
            record
            for record in self._records
            if record.subject_id == subject_id
        )

    def records_for_source(
        self,
        source_id: str,
    ) -> tuple[ExecutionProvenance, ...]:
        self._validate_filter_text("source_id", source_id)

        return tuple(
            record
            for record in self._records
            if record.source_id == source_id
        )

    @staticmethod
    def _validate_filter_text(
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