from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping

from models.execution_result_status import ExecutionResultStatus


@dataclass(frozen=True)
class ExecutionResult:
    execution_result_id: str
    execution_intent_id: str
    status: ExecutionResultStatus
    output: Mapping[str, Any]
    started_at: datetime
    completed_at: datetime
    error: str | None

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_result_id",
            self.execution_result_id,
        )
        self._validate_required_text(
            "execution_intent_id",
            self.execution_intent_id,
        )

        if not isinstance(self.status, ExecutionResultStatus):
            raise TypeError(
                "status must be an ExecutionResultStatus"
            )

        if self.started_at is None:
            raise ValueError("started_at must not be None")

        if not isinstance(self.started_at, datetime):
            raise TypeError("started_at must be a datetime")

        if self.completed_at is None:
            raise ValueError("completed_at must not be None")

        if not isinstance(self.completed_at, datetime):
            raise TypeError("completed_at must be a datetime")

        if self.completed_at < self.started_at:
            raise ValueError(
                "completed_at must not be before started_at"
            )

        if not isinstance(self.output, Mapping):
            raise TypeError("output must be a mapping")

        immutable_output = MappingProxyType(
            dict(self.output)
        )

        object.__setattr__(
            self,
            "output",
            immutable_output,
        )

        if self.error is not None and not isinstance(
            self.error,
            str,
        ):
            raise TypeError("error must be a string or None")

        if self.status is ExecutionResultStatus.SUCCEEDED:
            if self.error is not None:
                raise ValueError(
                    "successful result must not contain an error"
                )

        if self.status is ExecutionResultStatus.FAILED:
            if self.error is None or not self.error.strip():
                raise ValueError(
                    "failed result must contain an error"
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