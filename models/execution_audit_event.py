from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_audit_event_type import ExecutionAuditEventType


@dataclass(frozen=True)
class ExecutionAuditEvent:
    execution_audit_event_id: str
    execution_intent_id: str
    execution_result_id: str | None
    event_type: ExecutionAuditEventType
    occurred_at: datetime
    details: Mapping[str, Any]
    sequence_number: int

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_audit_event_id",
            self.execution_audit_event_id,
        )
        self._validate_required_text(
            "execution_intent_id",
            self.execution_intent_id,
        )

        if self.execution_result_id is not None:
            self._validate_required_text(
                "execution_result_id",
                self.execution_result_id,
            )

        if not isinstance(self.event_type, ExecutionAuditEventType):
            raise TypeError(
                "event_type must be an ExecutionAuditEventType"
            )

        if self.occurred_at is None:
            raise ValueError("occurred_at must not be None")

        if not isinstance(self.occurred_at, datetime):
            raise TypeError("occurred_at must be a datetime")

        if not isinstance(self.details, Mapping):
            raise TypeError("details must be a mapping")

        object.__setattr__(
            self,
            "details",
            MappingProxyType(dict(self.details)),
        )

        if not isinstance(self.sequence_number, int):
            raise TypeError("sequence_number must be an integer")

        if self.sequence_number <= 0:
            raise ValueError(
                "sequence_number must be greater than zero"
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