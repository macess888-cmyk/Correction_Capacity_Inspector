from __future__ import annotations

from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)


class ExecutionTransitionIntentRegistry:
    """Append-only registry for transition intents."""

    def __init__(self) -> None:
        self._intents: dict[str, ExecutionTransitionIntent] = {}

    def add(self, intent: ExecutionTransitionIntent) -> None:
        if intent.transition_id in self._intents:
            raise ValueError(
                f"Transition intent already exists: "
                f"{intent.transition_id}"
            )

        self._intents[intent.transition_id] = intent

    def get(
        self,
        transition_id: str,
    ) -> ExecutionTransitionIntent:
        if transition_id not in self._intents:
            raise KeyError(
                f"Transition intent not found: {transition_id}"
            )

        return self._intents[transition_id]

    def exists(self, transition_id: str) -> bool:
        return transition_id in self._intents

    def list(self) -> list[ExecutionTransitionIntent]:
        return list(self._intents.values())

    def list_for_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionTransitionIntent]:
        return [
            intent
            for intent in self._intents.values()
            if intent.execution_id == execution_id
        ]

    def count(self) -> int:
        return len(self._intents)