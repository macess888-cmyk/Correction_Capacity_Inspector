from datetime import datetime, timezone

import pytest

from models.execution_intent import ExecutionIntent
from models.execution_policy_evaluation import ExecutionPolicyEvaluation
from models.execution_policy_status import ExecutionPolicyStatus
from services.execution_policy_service import ExecutionPolicyService


def make_intent(
    *,
    action: str = "reconcile",
    target: str = "system-state",
) -> ExecutionIntent:
    return ExecutionIntent(
        execution_intent_id="INTENT-001",
        action=action,
        target=target,
        parameters={
            "mode": "bounded",
        },
        requested_by="AUTHORITY-001",
        created_at=datetime.now(timezone.utc),
        admissibility_id="ADMISSIBILITY-001",
    )


def test_service_evaluates_registered_policy():
    service = ExecutionPolicyService()

    def target_policy(intent: ExecutionIntent):
        return (
            ExecutionPolicyStatus.SATISFIED,
            "target is permitted",
            {
                "target": intent.target,
            },
        )

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=target_policy,
    )

    evaluation = service.evaluate(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        intent=make_intent(),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert isinstance(evaluation, ExecutionPolicyEvaluation)
    assert evaluation.execution_policy_id == "POLICY-001"
    assert evaluation.execution_intent_id == "INTENT-001"
    assert evaluation.status is ExecutionPolicyStatus.SATISFIED
    assert evaluation.reason == "target is permitted"
    assert evaluation.evidence["target"] == "system-state"


def test_service_records_violated_policy_truthfully():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.VIOLATED,
            "target is prohibited",
            {
                "target": intent.target,
            },
        ),
    )

    evaluation = service.evaluate(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        intent=make_intent(target="restricted-state"),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert evaluation.status is ExecutionPolicyStatus.VIOLATED
    assert evaluation.reason == "target is prohibited"


def test_service_records_not_applicable_policy():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.NOT_APPLICABLE,
            "policy does not apply",
            {},
        ),
    )

    evaluation = service.evaluate(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        intent=make_intent(),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert evaluation.status is ExecutionPolicyStatus.NOT_APPLICABLE


def test_service_rejects_unknown_policy():
    service = ExecutionPolicyService()

    with pytest.raises(ValueError):
        service.evaluate(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-UNKNOWN",
            intent=make_intent(),
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_requires_execution_intent():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.SATISFIED,
            "target is permitted",
            {},
        ),
    )

    with pytest.raises(TypeError):
        service.evaluate(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            intent="not-an-intent",
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_rejects_empty_policy_id():
    service = ExecutionPolicyService()

    with pytest.raises(ValueError):
        service.register_policy(
            execution_policy_id="",
            evaluator=lambda intent: (
                ExecutionPolicyStatus.SATISFIED,
                "target is permitted",
                {},
            ),
        )


def test_service_rejects_non_callable_evaluator():
    service = ExecutionPolicyService()

    with pytest.raises(TypeError):
        service.register_policy(
            execution_policy_id="POLICY-001",
            evaluator="not-callable",
        )


def test_service_rejects_duplicate_policy_registration():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.SATISFIED,
            "target is permitted",
            {},
        ),
    )

    with pytest.raises(ValueError):
        service.register_policy(
            execution_policy_id="POLICY-001",
            evaluator=lambda intent: (
                ExecutionPolicyStatus.SATISFIED,
                "target is permitted",
                {},
            ),
        )


def test_service_rejects_invalid_evaluator_status():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            "SATISFIED",
            "target is permitted",
            {},
        ),
    )

    with pytest.raises(TypeError):
        service.evaluate(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            intent=make_intent(),
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_rejects_invalid_evaluator_reason():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.SATISFIED,
            "",
            {},
        ),
    )

    with pytest.raises(ValueError):
        service.evaluate(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            intent=make_intent(),
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_rejects_non_mapping_evidence():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.SATISFIED,
            "target is permitted",
            "invalid",
        ),
    )

    with pytest.raises(TypeError):
        service.evaluate(
            execution_policy_evaluation_id="POLICY-EVAL-001",
            execution_policy_id="POLICY-001",
            intent=make_intent(),
            evaluated_at=datetime.now(timezone.utc),
        )


def test_policy_evaluation_does_not_authorize_execution():
    service = ExecutionPolicyService()

    service.register_policy(
        execution_policy_id="POLICY-001",
        evaluator=lambda intent: (
            ExecutionPolicyStatus.SATISFIED,
            "target is permitted",
            {},
        ),
    )

    evaluation = service.evaluate(
        execution_policy_evaluation_id="POLICY-EVAL-001",
        execution_policy_id="POLICY-001",
        intent=make_intent(),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert not hasattr(evaluation, "authorized")
    assert not hasattr(evaluation, "admissible")
    assert not hasattr(evaluation, "executed_at")