from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_policy_evaluation import ExecutionPolicyEvaluation
from models.execution_policy_status import ExecutionPolicyStatus


def make_policy_evaluation() -> ExecutionPolicyEvaluation:
    return ExecutionPolicyEvaluation(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        execution_intent_id="INTENT-001",
        status=ExecutionPolicyStatus.SATISFIED,
        evaluated_at=datetime.now(timezone.utc),
        reason="target is permitted",
        evidence={
            "target": "system-state",
        },
    )


def test_execution_policy_evaluation_can_be_created():
    evaluation = make_policy_evaluation()

    assert (
        evaluation.execution_policy_evaluation_id
        == "POLICY-EVAL-001"
    )
    assert evaluation.execution_policy_id == "POLICY-001"
    assert evaluation.execution_intent_id == "INTENT-001"
    assert evaluation.status is ExecutionPolicyStatus.SATISFIED
    assert evaluation.reason == "target is permitted"
    assert evaluation.evidence["target"] == "system-state"


def test_execution_policy_evaluation_is_immutable():
    evaluation = make_policy_evaluation()

    with pytest.raises(FrozenInstanceError):
        evaluation.status = ExecutionPolicyStatus.VIOLATED


def test_execution_policy_evidence_is_immutable():
    evaluation = make_policy_evaluation()

    with pytest.raises(TypeError):
        evaluation.evidence["target"] = "other-state"


def test_execution_policy_evidence_is_defensively_copied():
    evidence = {
        "target": "system-state",
    }

    evaluation = ExecutionPolicyEvaluation(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        execution_intent_id="INTENT-001",
        status=ExecutionPolicyStatus.SATISFIED,
        evaluated_at=datetime.now(timezone.utc),
        reason="target is permitted",
        evidence=evidence,
    )

    evidence["target"] = "other-state"

    assert evaluation.evidence["target"] == "system-state"


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_policy_evaluation_id",
        "execution_policy_id",
        "execution_intent_id",
        "reason",
    ],
)
def test_execution_policy_evaluation_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_policy_evaluation_id": "POLICY-EVAL-001",
        "execution_policy_id": "POLICY-001",
        "execution_intent_id": "INTENT-001",
        "status": ExecutionPolicyStatus.SATISFIED,
        "evaluated_at": datetime.now(timezone.utc),
        "reason": "target is permitted",
        "evidence": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionPolicyEvaluation(**values)


def test_execution_policy_evaluation_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionPolicyEvaluation(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            execution_intent_id="INTENT-001",
            status="SATISFIED",
            evaluated_at=datetime.now(timezone.utc),
            reason="target is permitted",
            evidence={},
        )


def test_execution_policy_evaluation_rejects_missing_evaluated_at():
    with pytest.raises(ValueError):
        ExecutionPolicyEvaluation(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            execution_intent_id="INTENT-001",
            status=ExecutionPolicyStatus.SATISFIED,
            evaluated_at=None,
            reason="target is permitted",
            evidence={},
        )


def test_execution_policy_evaluation_rejects_non_mapping_evidence():
    with pytest.raises(TypeError):
        ExecutionPolicyEvaluation(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            execution_intent_id="INTENT-001",
            status=ExecutionPolicyStatus.SATISFIED,
            evaluated_at=datetime.now(timezone.utc),
            reason="target is permitted",
            evidence="invalid",
        )


def test_execution_policy_evaluation_contains_no_authority_state():
    evaluation = make_policy_evaluation()

    assert not hasattr(evaluation, "authorized")
    assert not hasattr(evaluation, "admissible")
    assert not hasattr(evaluation, "refused")


def test_execution_policy_evaluation_contains_no_execution_state():
    evaluation = make_policy_evaluation()

    assert not hasattr(evaluation, "executed_at")
    assert not hasattr(evaluation, "result_id")
    assert not hasattr(evaluation, "receipt_id")