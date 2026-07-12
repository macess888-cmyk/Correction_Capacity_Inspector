from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class ExecutionReplay:
    execution_replay_id: str
    source_execution_intent_id: str
    source_execution_result_id: str
    action: str
    target: str
    parameters: Mapping[str, Any]
    requested_at: datetime
    requested_by: str
    reason: str

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_replay_id",
            self.execution_replay_id,
        )
        self._validate_required_text(
            "source_execution_intent_id",
            self.source_execution_intent_id,
        )
        self._validate_required_text(
            "source_execution_result_id",
            self.source_execution_result_id,
        )
        self._validate_required_text(
            "action",
            self.action,
        )
        self._validate_required_text(
            "target",
            self.target,
        )
        self._validate_required_text(
            "requested_by",
            self.requested_by,
        )
        self._validate_required_text(
            "reason",
            self.reason,
        )

        if self.requested_at is None:
            raise ValueError("requested_at must not be None")

        if not isinstance(self.requested_at, datetime):
            raise TypeError("requested_at must be a datetime")

        if not isinstance(self.parameters, Mapping):
            raise TypeError("parameters must be a mapping")

        object.__setattr__(
            self,
            "parameters",
            MappingProxyType(dict(self.parameters)),
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