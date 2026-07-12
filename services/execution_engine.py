from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any

from models.execution_intent import ExecutionIntent
from models.execution_result import ExecutionResult
from models.execution_result_status import ExecutionResultStatus


ExecutionHandler = Callable[
    [ExecutionIntent],
    Mapping[str, Any],
]


class ExecutionEngine:
    """Executes explicit intents through registered action handlers."""

    def __init__(self) -> None:
        self._handlers: dict[str, ExecutionHandler] = {}

    def register_handler(
        self,
        *,
        action: str,
        handler: ExecutionHandler,
    ) -> None:
        if not isinstance(action, str):
            raise TypeError("action must be a string")

        if not action.strip():
            raise ValueError("action must not be empty")

        if not callable(handler):
            raise TypeError("handler must be callable")

        if action in self._handlers:
            raise ValueError(
                f"handler already registered for action: {action}"
            )

        self._handlers[action] = handler

    def execute(
        self,
        *,
        execution_result_id: str,
        intent: ExecutionIntent,
    ) -> ExecutionResult:
        if not isinstance(intent, ExecutionIntent):
            raise TypeError(
                "intent must be an ExecutionIntent"
            )

        if not isinstance(execution_result_id, str):
            raise TypeError(
                "execution_result_id must be a string"
            )

        if not execution_result_id.strip():
            raise ValueError(
                "execution_result_id must not be empty"
            )

        handler = self._handlers.get(intent.action)

        if handler is None:
            raise ValueError(
                f"no handler registered for action: {intent.action}"
            )

        started_at = datetime.now(timezone.utc)

        try:
            output = handler(intent)

            if not isinstance(output, Mapping):
                raise TypeError(
                    "handler output must be a mapping"
                )

            completed_at = datetime.now(timezone.utc)

            return ExecutionResult(
                execution_result_id=execution_result_id,
                execution_intent_id=intent.execution_intent_id,
                status=ExecutionResultStatus.SUCCEEDED,
                output=output,
                started_at=started_at,
                completed_at=completed_at,
                error=None,
            )

        except Exception as error:
            completed_at = datetime.now(timezone.utc)

            return ExecutionResult(
                execution_result_id=execution_result_id,
                execution_intent_id=intent.execution_intent_id,
                status=ExecutionResultStatus.FAILED,
                output={},
                started_at=started_at,
                completed_at=completed_at,
                error=str(error),
            )