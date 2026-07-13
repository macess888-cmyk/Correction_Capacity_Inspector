from datetime import datetime, timezone

import pytest

from models.execution_reliance_decision import (
    ExecutionRelianceDecision,
)
from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)
from models.execution_reliance_evaluation import (
    ExecutionRelianceEvaluation,
)
from models.execution_reliance_status import ExecutionRelianceStatus
from services.execution_reliance_decision_service import (
    ExecutionRelianceDecisionService,
)


def make_evaluation(
    *,
    status: ExecutionRelianceStatus = ExecutionRelianceStatus.RELIABLE,
) -> ExecutionRelianceEvaluation:
    conditions = ()

    if status is ExecutionRelianceStatus.CONDITIONALLY_RELIABLE:
        conditions = (
            "manual review required",
        )

    return ExecutionRelianceEvaluation(
        execution_reliance_evaluation_id="RELIANCE-001",
        subject_id="ATTESTATION-001",
        standing_inspection_id="STANDING-001",
        status=status,
        evaluated_at=datetime.now(timezone.utc),
        reason="reliance evaluation completed",
        conditions=conditions,
        evidence_references=(
            "ATTESTATION-001",
            "STANDING-001",
        ),
        findings={},
    )


def test_service_accepts_reliable_evaluation():
    service = ExecutionRelianceDecisionService()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=make_evaluation(
            status=ExecutionRelianceStatus.RELIABLE,
        ),
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert isinstance(decision, ExecutionRelianceDecision)
    assert decision.decision is ExecutionRelianceDecisionType.ACCEPT
    assert decision.subject_id == "ATTESTATION-001"
    assert decision.reliance_evaluation_id == "RELIANCE-001"
    assert decision.conditions == ()


def test_service_rejects_not_reliable_evaluation():
    service = ExecutionRelianceDecisionService()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=make_evaluation(
            status=ExecutionRelianceStatus.NOT_RELIABLE,
        ),
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert decision.decision is ExecutionRelianceDecisionType.REJECT
    assert decision.conditions == ()


def test_service_holds_indeterminate_evaluation():
    service = ExecutionRelianceDecisionService()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=make_evaluation(
            status=ExecutionRelianceStatus.INDETERMINATE,
        ),
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert decision.decision is ExecutionRelianceDecisionType.HOLD
    assert decision.conditions == ()


def test_service_conditionally_accepts_conditional_evaluation():
    service = ExecutionRelianceDecisionService()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=make_evaluation(
            status=ExecutionRelianceStatus.CONDITIONALLY_RELIABLE,
        ),
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert (
        decision.decision
        is ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT
    )
    assert decision.conditions == (
        "manual review required",
    )


def test_service_preserves_evidence_references():
    service = ExecutionRelianceDecisionService()

    evaluation = make_evaluation()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=evaluation,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert decision.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-001",
        "STANDING-001",
    )


def test_service_requires_reliance_evaluation():
    service = ExecutionRelianceDecisionService()

    with pytest.raises(TypeError):
        service.decide(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            evaluation="not-an-evaluation",
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
        )


def test_service_preserves_model_validation():
    service = ExecutionRelianceDecisionService()

    with pytest.raises(ValueError):
        service.decide(
            execution_reliance_decision_id="",
            evaluation=make_evaluation(),
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
        )


def test_service_does_not_modify_evaluation():
    service = ExecutionRelianceDecisionService()

    evaluation = make_evaluation(
        status=ExecutionRelianceStatus.CONDITIONALLY_RELIABLE,
    )

    original_status = evaluation.status
    original_conditions = evaluation.conditions
    original_references = evaluation.evidence_references

    service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=evaluation,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert evaluation.status is original_status
    assert evaluation.conditions == original_conditions
    assert evaluation.evidence_references == original_references


def test_reliance_decision_creates_no_execution_authority():
    service = ExecutionRelianceDecisionService()

    decision = service.decide(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        evaluation=make_evaluation(),
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
    )

    assert not hasattr(decision, "authorized")
    assert not hasattr(decision, "admissible")
    assert not hasattr(decision, "permission")