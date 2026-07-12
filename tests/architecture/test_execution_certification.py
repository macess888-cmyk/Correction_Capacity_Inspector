from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_certification import ExecutionCertification
from models.execution_certification_status import (
    ExecutionCertificationStatus,
)


def make_execution_certification() -> ExecutionCertification:
    return ExecutionCertification(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        status=ExecutionCertificationStatus.CERTIFIED,
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        reason="all required evidence is present",
        evidence_references=(
            "INTENT-001",
            "RESULT-001",
            "RECEIPT-001",
        ),
        findings={
            "receipt_present": True,
            "provenance_present": True,
        },
    )


def test_execution_certification_can_be_created():
    certification = make_execution_certification()

    assert certification.execution_certification_id == "CERT-001"
    assert certification.certification_profile_id == "PROFILE-001"
    assert certification.subject_id == "EXECUTION-001"
    assert (
        certification.status
        is ExecutionCertificationStatus.CERTIFIED
    )
    assert certification.evaluated_by == "CERTIFICATION-SERVICE"
    assert certification.reason == "all required evidence is present"
    assert certification.evidence_references == (
        "INTENT-001",
        "RESULT-001",
        "RECEIPT-001",
    )
    assert certification.findings["receipt_present"] is True


def test_execution_certification_is_immutable():
    certification = make_execution_certification()

    with pytest.raises(FrozenInstanceError):
        certification.status = (
            ExecutionCertificationStatus.NOT_CERTIFIED
        )


def test_execution_certification_findings_are_immutable():
    certification = make_execution_certification()

    with pytest.raises(TypeError):
        certification.findings["receipt_present"] = False


def test_execution_certification_defensively_copies_findings():
    findings = {
        "receipt_present": True,
    }

    certification = ExecutionCertification(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        status=ExecutionCertificationStatus.CERTIFIED,
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        reason="required evidence is present",
        evidence_references=("RECEIPT-001",),
        findings=findings,
    )

    findings["receipt_present"] = False

    assert certification.findings["receipt_present"] is True


def test_execution_certification_copies_evidence_references():
    references = [
        "INTENT-001",
        "RESULT-001",
    ]

    certification = ExecutionCertification(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        status=ExecutionCertificationStatus.CERTIFIED,
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        reason="required evidence is present",
        evidence_references=references,
        findings={},
    )

    references.append("RECEIPT-001")

    assert certification.evidence_references == (
        "INTENT-001",
        "RESULT-001",
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_certification_id",
        "certification_profile_id",
        "subject_id",
        "evaluated_by",
        "reason",
    ],
)
def test_execution_certification_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_certification_id": "CERT-001",
        "certification_profile_id": "PROFILE-001",
        "subject_id": "EXECUTION-001",
        "status": ExecutionCertificationStatus.CERTIFIED,
        "evaluated_at": datetime.now(timezone.utc),
        "evaluated_by": "CERTIFICATION-SERVICE",
        "reason": "all required evidence is present",
        "evidence_references": ("RECEIPT-001",),
        "findings": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionCertification(**values)


def test_execution_certification_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionCertification(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            status="CERTIFIED",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            reason="all required evidence is present",
            evidence_references=("RECEIPT-001",),
            findings={},
        )


def test_execution_certification_rejects_missing_evaluated_at():
    with pytest.raises(ValueError):
        ExecutionCertification(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            status=ExecutionCertificationStatus.CERTIFIED,
            evaluated_at=None,
            evaluated_by="CERTIFICATION-SERVICE",
            reason="all required evidence is present",
            evidence_references=("RECEIPT-001",),
            findings={},
        )


def test_execution_certification_rejects_empty_evidence_reference():
    with pytest.raises(ValueError):
        ExecutionCertification(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            status=ExecutionCertificationStatus.CERTIFIED,
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            reason="all required evidence is present",
            evidence_references=("RECEIPT-001", ""),
            findings={},
        )


def test_execution_certification_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionCertification(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            status=ExecutionCertificationStatus.CERTIFIED,
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            reason="all required evidence is present",
            evidence_references=(
                "RECEIPT-001",
                "RECEIPT-001",
            ),
            findings={},
        )


def test_execution_certification_rejects_non_mapping_findings():
    with pytest.raises(TypeError):
        ExecutionCertification(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            status=ExecutionCertificationStatus.CERTIFIED,
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            reason="all required evidence is present",
            evidence_references=("RECEIPT-001",),
            findings="invalid",
        )


def test_execution_certification_contains_no_future_authority():
    certification = make_execution_certification()

    assert not hasattr(certification, "authorized")
    assert not hasattr(certification, "admissible")
    assert not hasattr(certification, "permission")


def test_execution_certification_contains_no_execution_behavior():
    certification = make_execution_certification()

    assert not hasattr(certification, "execute")
    assert not hasattr(certification, "handler")
    assert not hasattr(certification, "receipt_id")