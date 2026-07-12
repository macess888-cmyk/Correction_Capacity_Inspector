from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_replay import ExecutionReplay


def make_execution_replay() -> ExecutionReplay:
    return ExecutionReplay(
        execution_replay_id="REPLAY-001",
        source_execution_intent_id="INTENT-001",
        source_execution_result_id="RESULT-001",
        action="reconcile",
        target="system-state",
        parameters={
            "mode": "bounded",
        },
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )


def test_execution_replay_can_be_created():
    replay = make_execution_replay()

    assert replay.execution_replay_id == "REPLAY-001"
    assert replay.source_execution_intent_id == "INTENT-001"
    assert replay.source_execution_result_id == "RESULT-001"
    assert replay.action == "reconcile"
    assert replay.target == "system-state"
    assert replay.parameters["mode"] == "bounded"
    assert replay.requested_by == "AUTHORITY-002"
    assert replay.reason == "verification replay"


def test_execution_replay_is_immutable():
    replay = make_execution_replay()

    with pytest.raises(FrozenInstanceError):
        replay.action = "stop"


def test_execution_replay_parameters_are_immutable():
    replay = make_execution_replay()

    with pytest.raises(TypeError):
        replay.parameters["mode"] = "unbounded"


def test_execution_replay_defensively_copies_parameters():
    parameters = {
        "mode": "bounded",
    }

    replay = ExecutionReplay(
        execution_replay_id="REPLAY-001",
        source_execution_intent_id="INTENT-001",
        source_execution_result_id="RESULT-001",
        action="reconcile",
        target="system-state",
        parameters=parameters,
        requested_at=datetime.now(timezone.utc),
        requested_by="AUTHORITY-002",
        reason="verification replay",
    )

    parameters["mode"] = "unbounded"

    assert replay.parameters["mode"] == "bounded"


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_replay_id",
        "source_execution_intent_id",
        "source_execution_result_id",
        "action",
        "target",
        "requested_by",
        "reason",
    ],
)
def test_execution_replay_rejects_empty_required_text(field_name):
    values = {
        "execution_replay_id": "REPLAY-001",
        "source_execution_intent_id": "INTENT-001",
        "source_execution_result_id": "RESULT-001",
        "action": "reconcile",
        "target": "system-state",
        "parameters": {},
        "requested_at": datetime.now(timezone.utc),
        "requested_by": "AUTHORITY-002",
        "reason": "verification replay",
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionReplay(**values)


def test_execution_replay_rejects_missing_requested_at():
    with pytest.raises(ValueError):
        ExecutionReplay(
            execution_replay_id="REPLAY-001",
            source_execution_intent_id="INTENT-001",
            source_execution_result_id="RESULT-001",
            action="reconcile",
            target="system-state",
            parameters={},
            requested_at=None,
            requested_by="AUTHORITY-002",
            reason="verification replay",
        )


def test_execution_replay_rejects_non_mapping_parameters():
    with pytest.raises(TypeError):
        ExecutionReplay(
            execution_replay_id="REPLAY-001",
            source_execution_intent_id="INTENT-001",
            source_execution_result_id="RESULT-001",
            action="reconcile",
            target="system-state",
            parameters="invalid",
            requested_at=datetime.now(timezone.utc),
            requested_by="AUTHORITY-002",
            reason="verification replay",
        )


def test_execution_replay_contains_no_authorization_state():
    replay = make_execution_replay()

    assert not hasattr(replay, "authorized")
    assert not hasattr(replay, "admissible")
    assert not hasattr(replay, "authorization_id")


def test_execution_replay_contains_no_execution_state():
    replay = make_execution_replay()

    assert not hasattr(replay, "status")
    assert not hasattr(replay, "executed_at")
    assert not hasattr(replay, "receipt_id")