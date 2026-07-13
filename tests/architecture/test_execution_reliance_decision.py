from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_reliance_decision import (
    ExecutionRelianceDecision,
)
from models.execution_reliance_decision_type import (
    ExecutionRelianceDecisionType,
)


def make_decision() -> ExecutionRelianceDecision:
    return ExecutionRelianceDecision(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        subject_id="ATTESTATION-001",
        reliance_evaluation_id="RELIANCE-001",
        decision=ExecutionRelianceDecisionType.ACCEPT,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
        reason="current reliance is supported",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-001",
        ),
        metadata={
            "scope": "present-use",
        },
    )


def test_execution_reliance_decision_can_be_created():
    decision = make_decision()

    assert (
        decision.execution_reliance_decision_id
        == "RELIANCE-DECISION-001"
    )
    assert decision.subject_id == "ATTESTATION-001"
    assert decision.reliance_evaluation_id == "RELIANCE-001"
    assert decision.decision is ExecutionRelianceDecisionType.ACCEPT
    assert decision.decided_by == "GOVERNANCE-001"
    assert decision.conditions == ()
    assert decision.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-001",
    )
    assert decision.metadata["scope"] == "present-use"


def test_execution_reliance_decision_is_immutable():
    decision = make_decision()

    with pytest.raises(FrozenInstanceError):
        decision.decision = ExecutionRelianceDecisionType.REJECT


def test_execution_reliance_decision_metadata_is_immutable():
    decision = make_decision()

    with pytest.raises(TypeError):
        decision.metadata["scope"] = "changed"


def test_execution_reliance_decision_defensively_copies_metadata():
    metadata = {
        "scope": "present-use",
    }

    decision = ExecutionRelianceDecision(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        subject_id="ATTESTATION-001",
        reliance_evaluation_id="RELIANCE-001",
        decision=ExecutionRelianceDecisionType.ACCEPT,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
        reason="current reliance is supported",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-001",
        ),
        metadata=metadata,
    )

    metadata["scope"] = "changed"

    assert decision.metadata["scope"] == "present-use"


def test_execution_reliance_decision_copies_conditions():
    conditions = [
        "manual review required",
    ]

    decision = ExecutionRelianceDecision(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        subject_id="ATTESTATION-001",
        reliance_evaluation_id="RELIANCE-001",
        decision=ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
        reason="reliance accepted with controls",
        conditions=conditions,
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-001",
        ),
        metadata={},
    )

    conditions.append("secondary approval required")

    assert decision.conditions == (
        "manual review required",
    )


def test_execution_reliance_decision_copies_evidence_references():
    references = [
        "ATTESTATION-001",
        "RELIANCE-001",
    ]

    decision = ExecutionRelianceDecision(
        execution_reliance_decision_id="RELIANCE-DECISION-001",
        subject_id="ATTESTATION-001",
        reliance_evaluation_id="RELIANCE-001",
        decision=ExecutionRelianceDecisionType.ACCEPT,
        decided_at=datetime.now(timezone.utc),
        decided_by="GOVERNANCE-001",
        reason="current reliance is supported",
        conditions=(),
        evidence_references=references,
        metadata={},
    )

    references.append("STANDING-001")

    assert decision.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-001",
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_reliance_decision_id",
        "subject_id",
        "reliance_evaluation_id",
        "decided_by",
        "reason",
    ],
)
def test_execution_reliance_decision_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_reliance_decision_id": "RELIANCE-DECISION-001",
        "subject_id": "ATTESTATION-001",
        "reliance_evaluation_id": "RELIANCE-001",
        "decision": ExecutionRelianceDecisionType.ACCEPT,
        "decided_at": datetime.now(timezone.utc),
        "decided_by": "GOVERNANCE-001",
        "reason": "current reliance is supported",
        "conditions": (),
        "evidence_references": (
            "ATTESTATION-001",
            "RELIANCE-001",
        ),
        "metadata": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionRelianceDecision(**values)


def test_execution_reliance_decision_rejects_invalid_type():
    with pytest.raises(TypeError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision="ACCEPT",
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
            ),
            metadata={},
        )


def test_execution_reliance_decision_rejects_missing_decided_at():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=None,
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
            ),
            metadata={},
        )


def test_conditional_accept_requires_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.CONDITIONAL_ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="controls are required",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
            ),
            metadata={},
        )


def test_non_conditional_decision_rejects_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=("manual review required",),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
            ),
            metadata={},
        )


def test_execution_reliance_decision_requires_subject_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=("RELIANCE-001",),
            metadata={},
        )


def test_execution_reliance_decision_requires_evaluation_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=("ATTESTATION-001",),
            metadata={},
        )


def test_execution_reliance_decision_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
                "RELIANCE-001",
            ),
            metadata={},
        )


def test_execution_reliance_decision_rejects_non_mapping_metadata():
    with pytest.raises(TypeError):
        ExecutionRelianceDecision(
            execution_reliance_decision_id="RELIANCE-DECISION-001",
            subject_id="ATTESTATION-001",
            reliance_evaluation_id="RELIANCE-001",
            decision=ExecutionRelianceDecisionType.ACCEPT,
            decided_at=datetime.now(timezone.utc),
            decided_by="GOVERNANCE-001",
            reason="current reliance is supported",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-001",
            ),
            metadata="invalid",
        )


def test_execution_reliance_decision_contains_no_execution_behavior():
    decision = make_decision()

    assert not hasattr(decision, "execute")
    assert not hasattr(decision, "handler")
    assert not hasattr(decision, "result_id")


def test_execution_reliance_decision_contains_no_authorization_state():
    decision = make_decision()

    assert not hasattr(decision, "authorized")
    assert not hasattr(decision, "admissible")
    assert not hasattr(decision, "permission")