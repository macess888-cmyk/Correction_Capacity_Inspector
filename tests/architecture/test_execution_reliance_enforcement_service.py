from datetime import datetime, timezone

import pytest

from models.execution_reliance_decision import (
    ExecutionRelianceDecision,
)
from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)
from models.execution_reliance_enforcement import (
    ExecutionRelianceEnforcement,
)
from models.execution_reliance_enforcement_outcome import (
    ExecutionRelianceEnforcementOutcome,
)
from services.execution_reliance_enforcement_service import (
    ExecutionRelianceEnforcementService,
)


def make_decision(
    *,
    decision: ExecutionRelianceDecisionType = (
        ExecutionRelianceDecisionType.ACCEPT
    ),
) -> ExecutionRelianceDecision:
    conditions = ()

    if decision is ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT:
        conditions = (
            "manual review required",
        )

    return ExecutionRelianceDecision(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        subject_id="ATTESTATION-001",
        reliance_evaluation_id="RELIANCE-001",
        decision=decision,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
        reason="reliance decision completed",
        conditions=conditions,
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-001",
        ),
        metadata={},
    )


def test_service_maps_accept_to_permitted():
    service = ExecutionRelianceEnforcementService()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=make_decision(
            decision=ExecutionRelianceDecisionType.ACCEPT,
        ),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert isinstance(enforcement, ExecutionRelianceEnforcement)
    assert (
        enforcement.outcome
        is ExecutionRelianceEnforcementOutcome.PERMITTED
    )
    assert enforcement.subject_id == "ATTESTATION-001"
    assert (
        enforcement.reliance_decision_id
        == "RELIANCE-DECISION-001"
    )
    assert enforcement.conditions == ()


def test_service_maps_reject_to_blocked():
    service = ExecutionRelianceEnforcementService()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=make_decision(
            decision=ExecutionRelianceDecisionType.REJECT,
        ),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert (
        enforcement.outcome
        is ExecutionRelianceEnforcementOutcome.BLOCKED
    )
    assert enforcement.conditions == ()


def test_service_maps_hold_to_held():
    service = ExecutionRelianceEnforcementService()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=make_decision(
            decision=ExecutionRelianceDecisionType.HOLD,
        ),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert (
        enforcement.outcome
        is ExecutionRelianceEnforcementOutcome.HELD
    )
    assert enforcement.conditions == ()


def test_service_maps_conditional_accept():
    service = ExecutionRelianceEnforcementService()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=make_decision(
            decision=(
                ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT
            ),
        ),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert (
        enforcement.outcome
        is ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED
    )
    assert enforcement.conditions == (
        "manual review required",
    )


def test_service_preserves_evidence_references():
    service = ExecutionRelianceEnforcementService()

    decision = make_decision()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=decision,
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert enforcement.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-DECISION-001",
        "RELIANCE-001",
    )


def test_service_requires_reliance_decision():
    service = ExecutionRelianceEnforcementService()

    with pytest.raises(TypeError):
        service.enforce(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            decision="not-a-decision",
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
        )


def test_service_preserves_model_validation():
    service = ExecutionRelianceEnforcementService()

    with pytest.raises(ValueError):
        service.enforce(
            execution_reliance_enforcement_id="",
            decision=make_decision(),
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
        )


def test_service_does_not_modify_decision():
    service = ExecutionRelianceEnforcementService()

    decision = make_decision(
        decision=ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT,
    )

    original_decision = decision.decision
    original_conditions = decision.conditions
    original_references = decision.evidence_references

    service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=decision,
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert decision.decision is original_decision
    assert decision.conditions == original_conditions
    assert decision.evidence_references == original_references


def test_enforcement_creates_no_execution_authority():
    service = ExecutionRelianceEnforcementService()

    enforcement = service.enforce(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        decision=make_decision(),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
    )

    assert not hasattr(enforcement, "authorized")
    assert not hasattr(enforcement, "admissible")
    assert not hasattr(enforcement, "permission")