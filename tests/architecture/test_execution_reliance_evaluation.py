from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_reliance_evaluation import (
    ExecutionRelianceEvaluation,
)
from models.execution_reliance_status import ExecutionRelianceStatus


def make_evaluation() -> ExecutionRelianceEvaluation:
    return ExecutionRelianceEvaluation(
        execution_reliance_evaluation_id="RELIANCE-001",
        subject_id="ATTESTATION-001",
        standing_inspection_id="STANDING-001",
        status=ExecutionRelianceStatus.RELIABLE,
        evaluated_at=datetime.now(timezone.utc),
        reason="subject standing is active",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "STANDING-001",
        ),
        findings={
            "standing_status": "ACTIVE",
        },
    )


def test_execution_reliance_evaluation_can_be_created():
    evaluation = make_evaluation()

    assert (
        evaluation.execution_reliance_evaluation_id
        == "RELIANCE-001"
    )
    assert evaluation.subject_id == "ATTESTATION-001"
    assert evaluation.standing_inspection_id == "STANDING-001"
    assert evaluation.status is ExecutionRelianceStatus.RELIABLE
    assert evaluation.conditions == ()
    assert evaluation.evidence_references == (
        "ATTESTATION-001",
        "STANDING-001",
    )
    assert evaluation.findings["standing_status"] == "ACTIVE"


def test_execution_reliance_evaluation_is_immutable():
    evaluation = make_evaluation()

    with pytest.raises(FrozenInstanceError):
        evaluation.status = ExecutionRelianceStatus.NOT_RELIABLE


def test_execution_reliance_findings_are_immutable():
    evaluation = make_evaluation()

    with pytest.raises(TypeError):
        evaluation.findings["standing_status"] = "REVOKED"


def test_execution_reliance_findings_are_defensively_copied():
    findings = {
        "standing_status": "ACTIVE",
    }

    evaluation = ExecutionRelianceEvaluation(
        execution_reliance_evaluation_id="RELIANCE-001",
        subject_id="ATTESTATION-001",
        standing_inspection_id="STANDING-001",
        status=ExecutionRelianceStatus.RELIABLE,
        evaluated_at=datetime.now(timezone.utc),
        reason="subject standing is active",
        conditions=(),
        evidence_references=(
            "ATTESTATION-001",
            "STANDING-001",
        ),
        findings=findings,
    )

    findings["standing_status"] = "REVOKED"

    assert evaluation.findings["standing_status"] == "ACTIVE"


def test_execution_reliance_copies_conditions():
    conditions = [
        "manual review required",
    ]

    evaluation = ExecutionRelianceEvaluation(
        execution_reliance_evaluation_id="RELIANCE-001",
        subject_id="ATTESTATION-001",
        standing_inspection_id="STANDING-001",
        status=ExecutionRelianceStatus.CONDITIONALLY_RELIABLE,
        evaluated_at=datetime.now(timezone.utc),
        reason="reliance requires additional review",
        conditions=conditions,
        evidence_references=(
            "ATTESTATION-001",
            "STANDING-001",
        ),
        findings={},
    )

    conditions.append("secondary approval required")

    assert evaluation.conditions == (
        "manual review required",
    )


def test_execution_reliance_copies_evidence_references():
    references = [
        "ATTESTATION-001",
        "STANDING-001",
    ]

    evaluation = ExecutionRelianceEvaluation(
        execution_reliance_evaluation_id="RELIANCE-001",
        subject_id="ATTESTATION-001",
        standing_inspection_id="STANDING-001",
        status=ExecutionRelianceStatus.RELIABLE,
        evaluated_at=datetime.now(timezone.utc),
        reason="subject standing is active",
        conditions=(),
        evidence_references=references,
        findings={},
    )

    references.append("REVOCATION-001")

    assert evaluation.evidence_references == (
        "ATTESTATION-001",
        "STANDING-001",
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_reliance_evaluation_id",
        "subject_id",
        "standing_inspection_id",
        "reason",
    ],
)
def test_execution_reliance_rejects_empty_required_text(field_name):
    values = {
        "execution_reliance_evaluation_id": "RELIANCE-001",
        "subject_id": "ATTESTATION-001",
        "standing_inspection_id": "STANDING-001",
        "status": ExecutionRelianceStatus.RELIABLE,
        "evaluated_at": datetime.now(timezone.utc),
        "reason": "subject standing is active",
        "conditions": (),
        "evidence_references": (
            "ATTESTATION-001",
            "STANDING-001",
        ),
        "findings": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(**values)


def test_execution_reliance_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status="RELIABLE",
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
            ),
            findings={},
        )


def test_execution_reliance_rejects_missing_evaluated_at():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=None,
            reason="subject standing is active",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
            ),
            findings={},
        )


def test_conditional_reliance_requires_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.CONDITIONALLY_RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="additional review is required",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
            ),
            findings={},
        )


def test_non_conditional_reliance_rejects_conditions():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=("manual review required",),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
            ),
            findings={},
        )


def test_execution_reliance_requires_subject_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=(),
            evidence_references=("STANDING-001",),
            findings={},
        )


def test_execution_reliance_requires_standing_reference():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=(),
            evidence_references=("ATTESTATION-001",),
            findings={},
        )


def test_execution_reliance_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
                "STANDING-001",
            ),
            findings={},
        )


def test_execution_reliance_rejects_non_mapping_findings():
    with pytest.raises(TypeError):
        ExecutionRelianceEvaluation(
            execution_reliance_evaluation_id="RELIANCE-001",
            subject_id="ATTESTATION-001",
            standing_inspection_id="STANDING-001",
            status=ExecutionRelianceStatus.RELIABLE,
            evaluated_at=datetime.now(timezone.utc),
            reason="subject standing is active",
            conditions=(),
            evidence_references=(
                "ATTESTATION-001",
                "STANDING-001",
            ),
            findings="invalid",
        )


def test_execution_reliance_contains_no_authority_state():
    evaluation = make_evaluation()

    assert not hasattr(evaluation, "authorized")
    assert not hasattr(evaluation, "admissible")
    assert not hasattr(evaluation, "permission")


def test_execution_reliance_contains_no_execution_behavior():
    evaluation = make_evaluation()

    assert not hasattr(evaluation, "execute")
    assert not hasattr(evaluation, "handler")
    assert not hasattr(evaluation, "result_id")