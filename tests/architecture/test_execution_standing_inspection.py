from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_standing_inspection import (
    ExecutionStandingInspection,
)
from models.execution_standing_status import ExecutionStandingStatus


def make_inspection() -> ExecutionStandingInspection:
    return ExecutionStandingInspection(
        execution_standing_inspection_id="STANDING-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionStandingStatus.ACTIVE,
        inspected_at=datetime.now(timezone.utc),
        reason="no later revocation record applies",
        governing_record_id="ATTESTATION-001",
        evidence_references=("ATTESTATION-001",),
        findings={
            "revocation_count": 0,
        },
    )


def test_execution_standing_inspection_can_be_created():
    inspection = make_inspection()

    assert (
        inspection.execution_standing_inspection_id
        == "STANDING-001"
    )
    assert inspection.subject_id == "ATTESTATION-001"
    assert inspection.subject_type == "EXECUTION_ATTESTATION"
    assert inspection.status is ExecutionStandingStatus.ACTIVE
    assert inspection.governing_record_id == "ATTESTATION-001"
    assert inspection.evidence_references == ("ATTESTATION-001",)
    assert inspection.findings["revocation_count"] == 0


def test_execution_standing_inspection_is_immutable():
    inspection = make_inspection()

    with pytest.raises(FrozenInstanceError):
        inspection.status = ExecutionStandingStatus.REVOKED


def test_execution_standing_findings_are_immutable():
    inspection = make_inspection()

    with pytest.raises(TypeError):
        inspection.findings["revocation_count"] = 1


def test_execution_standing_findings_are_defensively_copied():
    findings = {
        "revocation_count": 0,
    }

    inspection = ExecutionStandingInspection(
        execution_standing_inspection_id="STANDING-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionStandingStatus.ACTIVE,
        inspected_at=datetime.now(timezone.utc),
        reason="no later revocation record applies",
        governing_record_id="ATTESTATION-001",
        evidence_references=("ATTESTATION-001",),
        findings=findings,
    )

    findings["revocation_count"] = 1

    assert inspection.findings["revocation_count"] == 0


def test_execution_standing_copies_evidence_references():
    references = [
        "ATTESTATION-001",
    ]

    inspection = ExecutionStandingInspection(
        execution_standing_inspection_id="STANDING-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionStandingStatus.ACTIVE,
        inspected_at=datetime.now(timezone.utc),
        reason="no later revocation record applies",
        governing_record_id="ATTESTATION-001",
        evidence_references=references,
        findings={},
    )

    references.append("REVOCATION-001")

    assert inspection.evidence_references == ("ATTESTATION-001",)


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_standing_inspection_id",
        "subject_id",
        "subject_type",
        "reason",
        "governing_record_id",
    ],
)
def test_execution_standing_rejects_empty_required_text(field_name):
    values = {
        "execution_standing_inspection_id": "STANDING-001",
        "subject_id": "ATTESTATION-001",
        "subject_type": "EXECUTION_ATTESTATION",
        "status": ExecutionStandingStatus.ACTIVE,
        "inspected_at": datetime.now(timezone.utc),
        "reason": "no later revocation record applies",
        "governing_record_id": "ATTESTATION-001",
        "evidence_references": ("ATTESTATION-001",),
        "findings": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionStandingInspection(**values)


def test_execution_standing_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status="ACTIVE",
            inspected_at=datetime.now(timezone.utc),
            reason="no later revocation record applies",
            governing_record_id="ATTESTATION-001",
            evidence_references=("ATTESTATION-001",),
            findings={},
        )


def test_execution_standing_rejects_missing_inspected_at():
    with pytest.raises(ValueError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionStandingStatus.ACTIVE,
            inspected_at=None,
            reason="no later revocation record applies",
            governing_record_id="ATTESTATION-001",
            evidence_references=("ATTESTATION-001",),
            findings={},
        )


def test_execution_standing_requires_subject_reference():
    with pytest.raises(ValueError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionStandingStatus.REVOKED,
            inspected_at=datetime.now(timezone.utc),
            reason="later revocation governs",
            governing_record_id="REVOCATION-001",
            evidence_references=("REVOCATION-001",),
            findings={},
        )


def test_execution_standing_requires_governing_record_reference():
    with pytest.raises(ValueError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionStandingStatus.REVOKED,
            inspected_at=datetime.now(timezone.utc),
            reason="later revocation governs",
            governing_record_id="REVOCATION-001",
            evidence_references=("ATTESTATION-001",),
            findings={},
        )


def test_execution_standing_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionStandingStatus.ACTIVE,
            inspected_at=datetime.now(timezone.utc),
            reason="no later revocation record applies",
            governing_record_id="ATTESTATION-001",
            evidence_references=(
                "ATTESTATION-001",
                "ATTESTATION-001",
            ),
            findings={},
        )


def test_execution_standing_rejects_non_mapping_findings():
    with pytest.raises(TypeError):
        ExecutionStandingInspection(
            execution_standing_inspection_id="STANDING-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionStandingStatus.ACTIVE,
            inspected_at=datetime.now(timezone.utc),
            reason="no later revocation record applies",
            governing_record_id="ATTESTATION-001",
            evidence_references=("ATTESTATION-001",),
            findings="invalid",
        )


def test_execution_standing_contains_no_authority_state():
    inspection = make_inspection()

    assert not hasattr(inspection, "authorized")
    assert not hasattr(inspection, "admissible")
    assert not hasattr(inspection, "permission")


def test_execution_standing_contains_no_mutation_behavior():
    inspection = make_inspection()

    assert not hasattr(inspection, "revoke")
    assert not hasattr(inspection, "suspend")
    assert not hasattr(inspection, "withdraw")