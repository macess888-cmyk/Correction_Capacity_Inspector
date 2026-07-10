from __future__ import annotations

from models.execution_consistency_record import (
    ExecutionConsistencyRecord,
)


class ExecutionConsistencyRecordRegistry:
    """Append-only registry for consistency records."""

    def __init__(self) -> None:
        self._records: dict[
            str,
            ExecutionConsistencyRecord,
        ] = {}

    def add(
        self,
        record: ExecutionConsistencyRecord,
    ) -> None:
        if record.record_id in self._records:
            raise ValueError(
                f"Consistency record already exists: "
                f"{record.record_id}"
            )

        self._records[record.record_id] = record

    def get(
        self,
        record_id: str,
    ) -> ExecutionConsistencyRecord:
        if record_id not in self._records:
            raise KeyError(
                f"Consistency record not found: {record_id}"
            )

        return self._records[record_id]

    def exists(self, record_id: str) -> bool:
        return record_id in self._records

    def list(self) -> list[ExecutionConsistencyRecord]:
        return list(self._records.values())

    def list_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionConsistencyRecord]:
        return [
            record
            for record in self._records.values()
            if record.execution_id == execution_id
        ]

    def count(self) -> int:
        return len(self._records)