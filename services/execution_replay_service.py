from __future__ import annotations

from datetime import datetime

from models.execution_intent import ExecutionIntent
from models.execution_replay import ExecutionReplay
from models.execution_result import ExecutionResult


class ExecutionReplayService:
    """Reconstructs replay candidates from matching historical evidence."""

    def create_replay(
        self,
        *,
        execution_replay_id: str,
        source_intent: ExecutionIntent,
        source_result: ExecutionResult,
        requested_at: datetime,
        requested_by: str,
        reason: str,
    ) -> ExecutionReplay:
        if not isinstance(source_intent, ExecutionIntent):
            raise TypeError(
                "source_intent must be an ExecutionIntent"
            )

        if not isinstance(source_result, ExecutionResult):
            raise TypeError(
                "source_result must be an ExecutionResult"
            )

        if (
            source_result.execution_intent_id
            != source_intent.execution_intent_id
        ):
            raise ValueError(
                "source_result must reference source_intent"
            )

        return ExecutionReplay(
            execution_replay_id=execution_replay_id,
            source_execution_intent_id=(
                source_intent.execution_intent_id
            ),
            source_execution_result_id=(
                source_result.execution_result_id
            ),
            action=source_intent.action,
            target=source_intent.target,
            parameters=source_intent.parameters,
            requested_at=requested_at,
            requested_by=requested_by,
            reason=reason,
        )