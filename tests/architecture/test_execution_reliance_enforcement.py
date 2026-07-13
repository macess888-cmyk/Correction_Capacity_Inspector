from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_reliance_enforcement import (
    ExecutionRelianceEnforcement,
)
from models.execution_reliance_enforcement_outcome import (
    ExecutionRelianceEnforcementOutcome,
)


def make_enforcement() -> ExecutionRelianceEnforcement:
    return ExecutionRelianceEnforcement(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        subject_id="ATTESTATION-001",
        reliance_decision_id="RELIANCE-DECISION-001",
        outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
        reason="reliance decision permits present use",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-DECISION-001",
        ),
        metadata={
            "scope": "present-use",
        },
    )


def test_execution_reliance_enforcement_can_be_created():
    enforcement = make_enforcement()

    assert (
        enforcement.execution_reliance_enforcement_id
        == "ENFORCEMENT-001"
    )
    assert enforcement.subject_id == "ATTESTATION-001"
    assert (
        enforcement.reliance_decision_id
        == "RELIANCE-DECISION-001"
    )
    assert (
        enforcement.outcome
        is ExecutionRelianceEnforcementOutcome.PERMITTED
    )
    assert enforcement.conditions == ()
    assert enforcement.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-DECISION-001",
    )
    assert enforcement.metadata["scope"] == "present-use"


def test_execution_reliance_enforcement_is_immutable():
    enforcement = make_enforcement()

    with pytest.raises(FrozenInstanceError):
        enforcement.outcome = (
            ExecutionRelianceEnforcementOutcome.BLOCKED
        )


def test_execution_reliance_enforcement_metadata_is_immutable():
    enforcement = make_enforcement()

    with pytest.raises(TypeError):
        enforcement.metadata["scope"] = "changed"


def test_execution_reliance_enforcement_defensively_copies_metadata():
    metadata = {
        "scope": "present-use",
    }

    enforcement = ExecutionRelianceEnforcement(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        subject_id="ATTESTATION-001",
        reliance_decision_id="RELIANCE-DECISION-001",
        outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
        reason="reliance decision permits present use",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-DECISION-001",
        ),
        metadata=metadata,
    )

    metadata["scope"] = "changed"

    assert enforcement.metadata["scope"] == "present-use"


def test_execution_reliance_enforcement_copies_conditions():
    conditions = [
        "manual review required",
    ]

    enforcement = ExecutionRelianceEnforcement(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        subject_id="ATTESTATION-001",
        reliance_decision_id="RELIANCE-DECISION-001",
        outcome=(
            ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED
        ),
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
        reason="present use is permitted subject to controls",
        conditions=conditions,
        evidence_references=(
            "ATTESTATION-001",
            "RELIANCE-DECISION-001",
        ),
        metadata={},
    )

    conditions.append("secondary approval required")

    assert enforcement.conditions == (
        "manual review required",
    )


def test_execution_reliance_enforcement_copies_evidence_references():
    references = [
        "ATTESTATION-001",
        "RELIANCE-DECISION-001",
    ]

    enforcement = ExecutionRelianceEnforcement(
        execution_reliance_enforcement_id="ENFORCEMENT-001",
        subject_id="ATTESTATION-001",
        reliance_decision_id="RELIANCE-DECISION-001",
        outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
        enforced_at=datetime.now(timezone.utc),
        enforced_by="ENFORCEMENT-SERVICE",
        reason="reliance decision permits present use",
        conditions=(),
        evidence_references=references,
        metadata={},
    )

    references.append("RELIANCE-001")

    assert enforcement.evidence_references == (
        "ATTESTATION-001",
        "RELIANCE-DECISION-001",
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_reliance_enforcement_id",
        "subject_id",
        "reliance_decision_id",
        "enforced_by",
        "reason",
    ],
)
def test_execution_reliance_enforcement_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_reliance_enforcement_id": "ENFORCEMENT-001",
        "subject_id": "ATTESTATION-001",
        "reliance_decision_id": "RELIANCE-DECISION-001",
        "outcome": ExecutionRelianceEnforcementOutcome.PERMITTED,
        "enforced_at": datetime.now(timezone.utc),
        "enforced_by": "ENFORCEMENT-SERVICE",
        "reason": "reliance decision permits present use",
        "conditions": (),
        "evidence_references": (
            "ATTESTATION-001",
            "RELIANCE-DECISION-001",
        ),
        "metadata": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(**values)


def test_execution_reliance_enforcement_rejects_invalid_outcome():
    with pytest.raises(TypeError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome="PERMITTED",
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata={},
        )


def test_execution_reliance_enforcement_rejects_missing_enforced_at():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=None,
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata={},
        )


def test_conditional_enforcement_requires_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=(
                ExecutionRelianceEnforcementOutcome.CONDITIONALLY_PERMITTED
            ),
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="controls are required",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata={},
        )


def test_non_conditional_enforcement_rejects_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=("manual review required",),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata={},
        )


def test_execution_reliance_enforcement_requires_subject_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=("RELIANCE-DECISION-001",),
            metadata={},
        )


def test_execution_reliance_enforcement_requires_decision_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=("ATTESTATION-001",),
            metadata={},
        )


def test_execution_reliance_enforcement_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata={},
        )


def test_execution_reliance_enforcement_rejects_non_mapping_metadata():
    with pytest.raises(TypeError):
        ExecutionRelianceEnforcement(
            execution_reliance_enforcement_id="ENFORCEMENT-001",
            subject_id="ATTESTATION-001",
            reliance_decision_id="RELIANCE-DECISION-001",
            outcome=ExecutionRelianceEnforcementOutcome.PERMITTED,
            enforced_at=datetime.now(timezone.utc),
            enforced_by="ENFORCEMENT-SERVICE",
            reason="reliance decision permits present use",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "RELIANCE-DECISION-001",
            ),
            metadata="invalid",
        )


def test_execution_reliance_enforcement_contains_no_execution_behavior():
    enforcement = make_enforcement()

    assert not hasattr(enforcement, "execute")
    assert not hasattr(enforcement, "handler")
    assert not hasattr(enforcement, "result_id")


def test_execution_reliance_enforcement_contains_no_authorization_state():
    enforcement = make_enforcement()

    assert not hasattr(enforcement, "authorized")
    assert not hasattr(enforcement, "admissible")
    assert not hasattr(enforcement, "permission")