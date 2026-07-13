from datetime import datetime, timezone

import pytest

from models.execution_attestation import ExecutionAttestation
from models.execution_attestation_status import (
    ExecutionAttestationStatus,
)
from models.execution_certification import ExecutionCertification
from models.execution_certification_status import (
    ExecutionCertificationStatus,
)
from services.execution_attestation_service import (
    ExecutionAttestationService,
)


def make_certification() -> ExecutionCertification:
    return ExecutionCertification(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        status=ExecutionCertificationStatus.CERTIFIED,
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        reason="required evidence is present",
        evidence_references=(
            "INTENT-001",
            "RESULT-001",
            "RECEIPT-001",
        ),
        findings={
            "receipt_present": True,
        },
    )


def test_service_creates_attestation_from_certification():
    service = ExecutionAttestationService()

    attestation = service.attest(
        execution_attestation_id="ATTESTATION-001",
        certification=make_certification(),
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was independently reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=(
            "CERT-001",
            "RECEIPT-001",
        ),
        metadata={
            "review_scope": "bounded",
        },
    )

    assert isinstance(attestation, ExecutionAttestation)
    assert attestation.certification_id == "CERT-001"
    assert attestation.subject_id == "EXECUTION-001"
    assert (
        attestation.status
        is ExecutionAttestationStatus.AFFIRMED
    )


def test_service_requires_execution_certification():
    service = ExecutionAttestationService()

    with pytest.raises(TypeError):
        service.attest(
            execution_attestation_id="ATTESTATION-001",
            certification="not-a-certification",
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_service_preserves_certification_subject():
    service = ExecutionAttestationService()

    certification = make_certification()

    attestation = service.attest(
        execution_attestation_id="ATTESTATION-001",
        certification=certification,
        status=ExecutionAttestationStatus.WITHHELD,
        statement="Additional evidence is required.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert attestation.subject_id == certification.subject_id
    assert (
        attestation.certification_id
        == certification.execution_certification_id
    )


def test_service_records_declined_attestation_truthfully():
    service = ExecutionAttestationService()

    attestation = service.attest(
        execution_attestation_id="ATTESTATION-001",
        certification=make_certification(),
        status=ExecutionAttestationStatus.DECLINED,
        statement="The certification cannot be affirmed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert (
        attestation.status
        is ExecutionAttestationStatus.DECLINED
    )


def test_service_requires_certification_reference_in_evidence():
    service = ExecutionAttestationService()

    with pytest.raises(ValueError):
        service.attest(
            execution_attestation_id="ATTESTATION-001",
            certification=make_certification(),
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("RECEIPT-001",),
            metadata={},
        )


def test_service_preserves_model_validation():
    service = ExecutionAttestationService()

    with pytest.raises(ValueError):
        service.attest(
            execution_attestation_id="",
            certification=make_certification(),
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_attestation_does_not_modify_certification():
    service = ExecutionAttestationService()

    certification = make_certification()
    original_references = certification.evidence_references
    original_findings = dict(certification.findings)

    service.attest(
        execution_attestation_id="ATTESTATION-001",
        certification=certification,
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert certification.evidence_references == original_references
    assert dict(certification.findings) == original_findings


def test_attestation_does_not_create_authority():
    service = ExecutionAttestationService()

    attestation = service.attest(
        execution_attestation_id="ATTESTATION-001",
        certification=make_certification(),
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert not hasattr(attestation, "authorized")
    assert not hasattr(attestation, "admissible")
    assert not hasattr(attestation, "permission")