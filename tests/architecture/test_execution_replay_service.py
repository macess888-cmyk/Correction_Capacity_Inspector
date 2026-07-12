from datetime import datetime, timezone

import pytest

from models.execution_intent import ExecutionIntent
from models.execution_replay import ExecutionReplay
from models.execution_result import ExecutionResult
from models.execution_result_status import ExecutionResultStatus
from services.execution_replay_service import ExecutionReplayService


def make_intent() -> ExecutionIntent:
    return ExecutionIntent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters={
            "mode": "bounded",
        },
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )


def make_result() -> ExecutionResult:
    now = datetime.now(timezone.utc)

    return ExecutionResult(
        execution_result_id="RESULT-001",
        execution_intent_id="INTENT-001",
        status=ExecutionResultStatus.SUCCEEDED,
        output={
            "state": "reconciled",
        },
        started_at=now,
        completed_at=now,
        error=None,
    )


def test_service_creates_replay_from_matching_evidence():
    service = ExecutionReplayService()

    replay = service.create_replay(
        execution_replay_id="REPLAY-001",
        source_intent=make_intent(),
        source_result=make_result(),
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )

    assert isinstance(replay, ExecutionReplay)
    assert replay.source_execution_intent_id == "INTENT-001"
    assert replay.source_execution_result_id == "RESULT-001"
    assert replay.action == "reconcile"
    assert replay.target == "system-state"
    assert replay.parameters["mode"] == "bounded"


def test_service_rejects_mismatched_result():
    service = ExecutionReplayService()

    now = datetime.now(timezone.utc)

    mismatched_result = ExecutionResult(
        execution_result_id="RESULT-002",
        execution_intent_id="INTENT-999",
        status=ExecutionResultStatus.SUCCEEDED,
        output={},
        started_at=now,
        completed_at=now,
        error=None,
    )

    with pytest.raises(ValueError):
        service.create_replay(
            execution_replay_id="REPLAY-001",
            source_intent=make_intent(),
            source_result=mismatched_result,
            requested_at=datetime.now(timezone.utc),
            requested_by="AUTHORITY-002",
            reason="verification replay",
        )


def test_service_requires_execution_intent():
    service = ExecutionReplayService()

    with pytest.raises(TypeError):
        service.create_replay(
            execution_replay_id="REPLAY-001",
            source_intent="not-an-intent",
            source_result=make_result(),
            requested_at=datetime.now(timezone.utc),
            requested_by="AUTHORITY-002",
            reason="verification replay",
        )


def test_service_requires_execution_result():
    service = ExecutionReplayService()

    with pytest.raises(TypeError):
        service.create_replay(
            execution_replay_id="REPLAY-001",
            source_intent=make_intent(),
            source_result="not-a-result",
            requested_at=datetime.now(timezone.utc),
            requested_by="AUTHORITY-002",
            reason="verification replay",
        )


def test_service_preserves_historical_parameters():
    service = ExecutionReplayService()

    intent = make_intent()

    replay = service.create_replay(
        execution_replay_id="REPLAY-001",
        source_intent=intent,
        source_result=make_result(),
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )

    assert dict(replay.parameters) == dict(intent.parameters)


def test_service_does_not_copy_historical_admissibility():
    service = ExecutionReplayService()

    replay = service.create_replay(
        execution_replay_id="REPLAY-001",
        source_intent=make_intent(),
        source_result=make_result(),
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )

    assert not hasattr(replay, "admissibility_id")
    assert not hasattr(replay, "authorized")
    assert not hasattr(replay, "admissible")


def test_service_does_not_execute_replay():
    service = ExecutionReplayService()

    replay = service.create_replay(
        execution_replay_id="REPLAY-001",
        source_intent=make_intent(),
        source_result=make_result(),
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )

    assert not hasattr(replay, "status")
    assert not hasattr(replay, "output")
    assert not hasattr(replay, "executed_at")


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_replay_id",
        "requested_by",
        "reason",
    ],
)
def test_service_preserves_model_validation(field_name):
    service = ExecutionReplayService()

    values = {
        "execution_replay_id": "REPLAY-001",
        "source_intent": make_intent(),
        "source_result": make_result(),
        "requested_at": datetime.now(timezone.utc),
        "requested_by": "AUTHORITY-002",
        "reason": "verification replay",
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        service.create_replay(**values)