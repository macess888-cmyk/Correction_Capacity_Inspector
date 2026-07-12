from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class ExecutionIntent:
    execution_intent_id: str
    action: str
    target: str
    parameters: Mapping[str, Any]
    requested_by: str
    created_at: datetime
    admissibility_id: str

    def __post_init__(self) -> None:
        self._validate_required_text(
            "execution_intent_id",
            self.execution_intent_id,
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
            "admissibility_id",
            self.admissibility_id,
        )

        if self.created_at is None:
            raise ValueError("created_at must not be None")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

        if not isinstance(self.parameters, Mapping):
            raise TypeError("parameters must be a mapping")

        immutable_parameters = MappingProxyType(
            dict(self.parameters)
        )

        object.__setattr__(
            self,
            "parameters",
            immutable_parameters,
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