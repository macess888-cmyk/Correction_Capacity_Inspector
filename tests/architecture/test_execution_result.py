from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_result import ExecutionResult
from models.execution_result_status import ExecutionResultStatus


def make_execution_result() -> ExecutionResult:
    started_at = datetime.now(timezone.utc)
    completed_at = datetime.now(timezone.utc)

    return ExecutionResult(
        execution_result_id="RESULT-001",
        execution_intent_id="INTENT-001",
        status=ExecutionResultStatus.SUCCEEDED,
        output={
            "state": "reconciled",
        },
        started_at=started_at,
        completed_at=completed_at,
        error=None,
    )


def test_execution_result_can_be_created():
    result = make_execution_result()

    assert result.execution_result_id == "RESULT-001"
    assert result.execution_intent_id == "INTENT-001"
    assert result.status is ExecutionResultStatus.SUCCEEDED
    assert result.output["state"] == "reconciled"
    assert result.error is None


def test_execution_result_is_immutable():
    result = make_execution_result()

    with pytest.raises(FrozenInstanceError):
        result.status = ExecutionResultStatus.FAILED


def test_execution_result_output_is_immutable():
    result = make_execution_result()

    with pytest.raises(TypeError):
        result.output["state"] = "changed"


def test_execution_result_defensively_copies_output():
    output = {
        "state": "reconciled",
    }

    result = ExecutionResult(
        execution_result_id="RESULT-001",
        execution_intent_id="INTENT-001",
        status=ExecutionResultStatus.SUCCEEDED,
        output=output,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        error=None,
    )

    output["state"] = "changed"

    assert result.output["state"] == "reconciled"


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_result_id",
        "execution_intent_id",
    ],
)
def test_execution_result_rejects_empty_required_text(field_name):
    values = {
        "execution_result_id": "RESULT-001",
        "execution_intent_id": "INTENT-001",
        "status": ExecutionResultStatus.SUCCEEDED,
        "output": {},
        "started_at": datetime.now(timezone.utc),
        "completed_at": datetime.now(timezone.utc),
        "error": None,
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionResult(**values)


def test_execution_result_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status="SUCCEEDED",
            output={},
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
            error=None,
        )


def test_execution_result_rejects_missing_started_at():
    with pytest.raises(ValueError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status=ExecutionResultStatus.SUCCEEDED,
            output={},
            started_at=None,
            completed_at=datetime.now(timezone.utc),
            error=None,
        )


def test_execution_result_rejects_missing_completed_at():
    with pytest.raises(ValueError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status=ExecutionResultStatus.SUCCEEDED,
            output={},
            started_at=datetime.now(timezone.utc),
            completed_at=None,
            error=None,
        )


def test_execution_result_rejects_completion_before_start():
    started_at = datetime.now(timezone.utc)

    with pytest.raises(ValueError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status=ExecutionResultStatus.SUCCEEDED,
            output={},
            started_at=started_at,
            completed_at=datetime.min.replace(tzinfo=timezone.utc),
            error=None,
        )


def test_successful_result_rejects_error():
    with pytest.raises(ValueError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status=ExecutionResultStatus.SUCCEEDED,
            output={},
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
            error="unexpected failure",
        )


def test_failed_result_requires_error():
    with pytest.raises(ValueError):
        ExecutionResult(
            execution_result_id="RESULT-001",
            execution_intent_id="INTENT-001",
            status=ExecutionResultStatus.FAILED,
            output={},
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
            error=None,
        )


def test_failed_result_accepts_error():
    result = ExecutionResult(
        execution_result_id="RESULT-001",
        execution_intent_id="INTENT-001",
        status=ExecutionResultStatus.FAILED,
        output={},
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
        error="handler failed",
    )

    assert result.status is ExecutionResultStatus.FAILED
    assert result.error == "handler failed"