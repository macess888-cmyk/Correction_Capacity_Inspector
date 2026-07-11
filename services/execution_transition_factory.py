from __future__ import annotations

from typing import Any, Mapping

from models.execution_transition_intent import (
    ExecutionTransitionIntent,
)
from models.execution_transition_operation import (
    ExecutionTransitionOperation,
)
from models.inspection_execution_status import (
    InspectionExecutionStatus,
)
from registries.execution_transition_definition_registry import (
    ExecutionTransitionDefinitionRegistry,
)


class ExecutionTransitionFactory:
    """
    Builds immutable transition intents from execution grammar.

    The factory is deterministic and side-effect free.

    It does not inspect registries beyond the read-only grammar,
    validate transitions, mutate execution state, record events,
    generate identifiers, or establish authority.
    """

    def __init__(
        self,
        definition_registry: (
            ExecutionTransitionDefinitionRegistry
        ),
    ) -> None:
        self._definition_registry = definition_registry

    def build_transition(
        self,
        operation: ExecutionTransitionOperation,
        transition_id: str,
        execution_id: str,
        event_id: str,
        previous_status: InspectionExecutionStatus,
        message: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> ExecutionTransitionIntent:
        definition = self._definition_registry.get(
            operation
        )

        return ExecutionTransitionIntent(
            transition_id=transition_id,
            execution_id=execution_id,
            event_id=event_id,
            previous_status=previous_status,
            target_status=definition.target_status,
            event_type=definition.event_type,
            target_stage=definition.target_stage,
            message=(
                definition.default_message
                if message is None
                else message
            ),
            metadata=metadata or {},
        )