from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_intent import ExecutionIntent


def make_execution_intent() -> ExecutionIntent:
    return ExecutionIntent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters={
            "mode": "bounded",
            "attempt": 1,
        },
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )


def test_execution_intent_can_be_created():
    intent = make_execution_intent()

    assert intent.execution_intent_id == "INTENT-001"
    assert intent.action == "reconcile"
    assert intent.target == "system-state"
    assert intent.requested_by == "AUTHORITY-001"
    assert intent.admissibility_id == "ADMISSIBILITY-001"


def test_execution_intent_is_immutable():
    intent = make_execution_intent()

    with pytest.raises(FrozenInstanceError):
        intent.action = "stop"


def test_execution_intent_parameters_are_immutable():
    intent = make_execution_intent()

    with pytest.raises(TypeError):
        intent.parameters["mode"] = "unbounded"


@pytest.mark.parametrize(
    "field_name, invalid_value",
    [
        ("execution_intent_id", ""),
        ("action", ""),
        ("target", ""),
        ("requested_by", ""),
        ("admissibility_id", ""),
    ],
)
def test_execution_intent_rejects_empty_required_text(
    field_name,
    invalid_value,
):
    values = {
        "execution_intent_id": "INTENT-001",
        "action": "reconcile",
        "target": "system-state",
        "parameters": {},
        "requested_by": "AUTHORITY-001",
        "created_at": datetime.now(timezone.utc),
        "admissibility_id": "ADMISSIBILITY-001",
    }

    values[field_name] = invalid_value

    with pytest.raises(ValueError):
        ExecutionIntent(**values)


def test_execution_intent_rejects_missing_created_at():
    with pytest.raises(ValueError):
        ExecutionIntent(
            execution_intent_id="INTENT-001",
            action="reconcile",
            target="system-state",
            parameters={},
            requested_by="AUTHORITY-001",
            created_at=None,
            admissibility_id="ADMISSIBILITY-001",
        )


def test_execution_intent_defensively_copies_parameters():
    parameters = {
        "mode": "bounded",
    }

    intent = ExecutionIntent(
        execution_intent_id="INTENT-001",
        action="reconcile",
        target="system-state",
        parameters=parameters,
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )

    parameters["mode"] = "unbounded"

    assert intent.parameters["mode"] == "bounded"