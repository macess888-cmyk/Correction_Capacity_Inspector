from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from models.execution_intent import ExecutionIntent


class ExecutionIntentService:
    """Creates immutable execution intents without performing execution."""

    def create_intent(
        self,
        *,
        execution_intent_id: str,
        action: str,
        target: str,
        parameters: Mapping[str, Any],
        requested_by: str,
        created_at: datetime,
        admissibility_id: str,
    ) -> ExecutionIntent:
        return ExecutionIntent(
            execution_intent_id=execution_intent_id,
            action=action,
            target=target,
            parameters=parameters,
            requested_by=requested_by,
            created_at=created_at,
            admissibility_id=admissibility_id,
        )