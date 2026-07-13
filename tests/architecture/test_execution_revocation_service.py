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
from models.execution_revocation import ExecutionRevocation
from models.execution_revocation_status import (
    ExecutionRevocationStatus,
)
from services.execution_revocation_service import (
    ExecutionRevocationService,
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
        evidence_references=("INTENT-001", "RESULT-001"),
        findings={},
    )


def make_attestation() -> ExecutionAttestation:
    return ExecutionAttestation(
        execution_attestation_id="ATTESTATION-001",
        subject_id="EXECUTION-001",
        certification_id="CERT-001",
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )


def test_service_revokes_attestation():
    service = ExecutionRevocationService()

    revocation = service.revoke_attestation(
        execution_revocation_id="REVOCATION-001",
        attestation=make_attestation(),
        status=ExecutionRevocationStatus.REVOKED,
        reason="current standing withdrawn",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=(
            "ATTESTATION-001",
            "CERT-001",
        ),
        metadata={"scope": "current-reliance"},
    )

    assert isinstance(revocation, ExecutionRevocation)
    assert revocation.subject_id == "ATTESTATION-001"
    assert revocation.subject_type == "EXECUTION_ATTESTATION"


def test_service_revokes_certification():
    service = ExecutionRevocationService()

    revocation = service.revoke_certification(
        execution_revocation_id="REVOCATION-001",
        certification=make_certification(),
        status=ExecutionRevocationStatus.SUSPENDED,
        reason="supporting evidence requires review",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="CERTIFIER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert revocation.subject_id == "CERT-001"
    assert revocation.subject_type == "EXECUTION_CERTIFICATION"
    assert revocation.status is ExecutionRevocationStatus.SUSPENDED


def test_service_requires_attestation():
    service = ExecutionRevocationService()

    with pytest.raises(TypeError):
        service.revoke_attestation(
            execution_revocation_id="REVOCATION-001",
            attestation="not-an-attestation",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=("ATTESTATION-001",),
            metadata={},
        )


def test_service_requires_certification():
    service = ExecutionRevocationService()

    with pytest.raises(TypeError):
        service.revoke_certification(
            execution_revocation_id="REVOCATION-001",
            certification="not-a-certification",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="CERTIFIER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_service_requires_attestation_reference():
    service = ExecutionRevocationService()

    with pytest.raises(ValueError):
        service.revoke_attestation(
            execution_revocation_id="REVOCATION-001",
            attestation=make_attestation(),
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_service_requires_certification_reference():
    service = ExecutionRevocationService()

    with pytest.raises(ValueError):
        service.revoke_certification(
            execution_revocation_id="REVOCATION-001",
            certification=make_certification(),
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="CERTIFIER-001",
            evidence_references=("RESULT-001",),
            metadata={},
        )


def test_revocation_does_not_modify_attestation():
    service = ExecutionRevocationService()

    attestation = make_attestation()
    original_references = attestation.evidence_references

    service.revoke_attestation(
        execution_revocation_id="REVOCATION-001",
        attestation=attestation,
        status=ExecutionRevocationStatus.REVOKED,
        reason="standing withdrawn",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=("ATTESTATION-001",),
        metadata={},
    )

    assert attestation.evidence_references == original_references
    assert attestation.status is ExecutionAttestationStatus.AFFIRMED


def test_revocation_does_not_modify_certification():
    service = ExecutionRevocationService()

    certification = make_certification()
    original_references = certification.evidence_references

    service.revoke_certification(
        execution_revocation_id="REVOCATION-001",
        certification=certification,
        status=ExecutionRevocationStatus.WITHDRAWN,
        reason="certifier withdrew current standing",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="CERTIFIER-001",
        evidence_references=("CERT-001",),
        metadata={},
    )

    assert certification.evidence_references == original_references
    assert (
        certification.status
        is ExecutionCertificationStatus.CERTIFIED
    )


def test_revocation_contains_no_deletion_behavior():
    service = ExecutionRevocationService()

    revocation = service.revoke_attestation(
        execution_revocation_id="REVOCATION-001",
        attestation=make_attestation(),
        status=ExecutionRevocationStatus.REVOKED,
        reason="standing withdrawn",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=("ATTESTATION-001",),
        metadata={},
    )

    assert not hasattr(revocation, "delete")
    assert not hasattr(revocation, "purge")
    assert not hasattr(revocation, "remove")