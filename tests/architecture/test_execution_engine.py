from datetime import datetime, timezone

import pytest

from models.execution_intent import ExecutionIntent
from models.execution_result_status import ExecutionResultStatus
from services.execution_engine import ExecutionEngine


def make_intent(
    *,
    action: str = "reconcile",
) -> ExecutionIntent:
    return ExecutionIntent(
        execution_intent_id="INTENT-001",
        action=action,
        target="system-state",
        parameters={
            "mode": "bounded",
        },
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )


def test_engine_executes_registered_handler():
    engine = ExecutionEngine()

    def reconcile_handler(intent: ExecutionIntent):
        return {
            "target": intent.target,
            "state": "reconciled",
        }

    engine.register_handler(
        action="reconcile",
        handler=reconcile_handler,
    )

    intent = make_intent()

    result = engine.execute(
        execution_result_id="RESULT-001",
        intent=intent,
    )

    assert result.execution_result_id == "RESULT-001"
    assert result.execution_intent_id == "INTENT-001"
    assert result.status is ExecutionResultStatus.SUCCEEDED
    assert result.output["state"] == "reconciled"
    assert result.output["target"] == "system-state"
    assert result.error is None


def test_engine_rejects_unknown_action():
    engine = ExecutionEngine()

    with pytest.raises(ValueError):
        engine.execute(
            execution_result_id="RESULT-001",
            intent=make_intent(action="unknown"),
        )


def test_engine_requires_execution_intent():
    engine = ExecutionEngine()

    with pytest.raises(TypeError):
        engine.execute(
            execution_result_id="RESULT-001",
            intent="not-an-intent",
        )


def test_engine_rejects_empty_result_id():
    engine = ExecutionEngine()

    engine.register_handler(
        action="reconcile",
        handler=lambda intent: {},
    )

    with pytest.raises(ValueError):
        engine.execute(
            execution_result_id="",
            intent=make_intent(),
        )


def test_engine_preserves_intent():
    engine = ExecutionEngine()

    engine.register_handler(
        action="reconcile",
        handler=lambda intent: {
            "observed_action": intent.action,
        },
    )

    intent = make_intent()
    original_parameters = dict(intent.parameters)

    engine.execute(
        execution_result_id="RESULT-001",
        intent=intent,
    )

    assert intent.execution_intent_id == "INTENT-001"
    assert intent.action == "reconcile"
    assert dict(intent.parameters) == original_parameters


def test_engine_records_handler_failure_truthfully():
    engine = ExecutionEngine()

    def failing_handler(intent: ExecutionIntent):
        raise RuntimeError("reconciliation failed")

    engine.register_handler(
        action="reconcile",
        handler=failing_handler,
    )

    result = engine.execute(
        execution_result_id="RESULT-001",
        intent=make_intent(),
    )

    assert result.status is ExecutionResultStatus.FAILED
    assert dict(result.output) == {}
    assert result.error == "reconciliation failed"


def test_engine_rejects_non_mapping_handler_output():
    engine = ExecutionEngine()

    engine.register_handler(
        action="reconcile",
        handler=lambda intent: "invalid-output",
    )

    result = engine.execute(
        execution_result_id="RESULT-001",
        intent=make_intent(),
    )

    assert result.status is ExecutionResultStatus.FAILED
    assert dict(result.output) == {}
    assert result.error == "handler output must be a mapping"


def test_engine_rejects_empty_handler_action():
    engine = ExecutionEngine()

    with pytest.raises(ValueError):
        engine.register_handler(
            action="",
            handler=lambda intent: {},
        )


def test_engine_rejects_non_callable_handler():
    engine = ExecutionEngine()

    with pytest.raises(TypeError):
        engine.register_handler(
            action="reconcile",
            handler="not-callable",
        )


def test_engine_rejects_duplicate_handler_registration():
    engine = ExecutionEngine()

    engine.register_handler(
        action="reconcile",
        handler=lambda intent: {},
    )

    with pytest.raises(ValueError):
        engine.register_handler(
            action="reconcile",
            handler=lambda intent: {},
        )


def test_engine_does_not_create_receipt():
    engine = ExecutionEngine()

    engine.register_handler(
        action="reconcile",
        handler=lambda intent: {},
    )

    result = engine.execute(
        execution_result_id="RESULT-001",
        intent=make_intent(),
    )

    assert not hasattr(result, "receipt_id")
    assert not hasattr(result, "execution_receipt_id")