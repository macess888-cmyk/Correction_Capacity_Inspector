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
from models.execution_standing_inspection import (
    ExecutionStandingInspection,
)
from models.execution_standing_status import ExecutionStandingStatus
from services.execution_standing_inspection_service import (
    ExecutionStandingInspectionService,
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


def make_revocation(
    *,
    subject_id: str,
    subject_type: str,
    status: ExecutionRevocationStatus,
    execution_revocation_id: str = "REVOCATION-001",
) -> ExecutionRevocation:
    return ExecutionRevocation(
        execution_revocation_id=execution_revocation_id,
        subject_id=subject_id,
        subject_type=subject_type,
        status=status,
        reason="current standing changed",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=(subject_id,),
        metadata={},
    )


def test_service_reports_active_attestation_without_revocation():
    service = ExecutionStandingInspectionService()

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(),
        inspected_at=datetime.now(timezone.utc),
    )

    assert isinstance(inspection, ExecutionStandingInspection)
    assert inspection.status is ExecutionStandingStatus.ACTIVE
    assert inspection.governing_record_id == "ATTESTATION-001"
    assert inspection.evidence_references == ("ATTESTATION-001",)
    assert inspection.findings["revocation_count"] == 0


def test_service_reports_active_certification_without_revocation():
    service = ExecutionStandingInspectionService()

    inspection = service.inspect_certification(
        execution_standing_inspection_id="STANDING-001",
        certification=make_certification(),
        revocations=(),
        inspected_at=datetime.now(timezone.utc),
    )

    assert inspection.status is ExecutionStandingStatus.ACTIVE
    assert inspection.governing_record_id == "CERT-001"
    assert inspection.subject_type == "EXECUTION_CERTIFICATION"


@pytest.mark.parametrize(
    "revocation_status, standing_status",
    [
        (
            ExecutionRevocationStatus.REVOKED,
            ExecutionStandingStatus.REVOKED,
        ),
        (
            ExecutionRevocationStatus.SUSPENDED,
            ExecutionStandingStatus.SUSPENDED,
        ),
        (
            ExecutionRevocationStatus.WITHDRAWN,
            ExecutionStandingStatus.WITHDRAWN,
        ),
    ],
)
def test_service_maps_latest_attestation_revocation(
    revocation_status,
    standing_status,
):
    service = ExecutionStandingInspectionService()

    revocation = make_revocation(
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=revocation_status,
    )

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(revocation,),
        inspected_at=datetime.now(timezone.utc),
    )

    assert inspection.status is standing_status
    assert inspection.governing_record_id == "REVOCATION-001"
    assert inspection.evidence_references == (
        "ATTESTATION-001",
        "REVOCATION-001",
    )


def test_service_uses_latest_applicable_revocation():
    service = ExecutionStandingInspectionService()

    first = ExecutionRevocation(
        execution_revocation_id="REVOCATION-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.SUSPENDED,
        reason="review pending",
        revoked_at=datetime(2026, 7, 12, tzinfo=timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=("ATTESTATION-001",),
        metadata={},
    )

    second = ExecutionRevocation(
        execution_revocation_id="REVOCATION-002",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
        reason="standing terminated",
        revoked_at=datetime(2026, 7, 13, tzinfo=timezone.utc),
        revoked_by="REVIEWER-002",
        evidence_references=("ATTESTATION-001",),
        metadata={},
    )

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(second, first),
        inspected_at=datetime.now(timezone.utc),
    )

    assert inspection.status is ExecutionStandingStatus.REVOKED
    assert inspection.governing_record_id == "REVOCATION-002"
    assert inspection.findings["revocation_count"] == 2


def test_service_ignores_revocation_for_other_subject():
    service = ExecutionStandingInspectionService()

    unrelated = make_revocation(
        subject_id="ATTESTATION-999",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
    )

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(unrelated,),
        inspected_at=datetime.now(timezone.utc),
    )

    assert inspection.status is ExecutionStandingStatus.ACTIVE
    assert inspection.findings["revocation_count"] == 0


def test_service_reports_indeterminate_for_subject_type_mismatch():
    service = ExecutionStandingInspectionService()

    mismatched = make_revocation(
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_CERTIFICATION",
        status=ExecutionRevocationStatus.REVOKED,
    )

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(mismatched,),
        inspected_at=datetime.now(timezone.utc),
    )

    assert inspection.status is ExecutionStandingStatus.INDETERMINATE
    assert inspection.governing_record_id == "REVOCATION-001"


def test_service_requires_attestation():
    service = ExecutionStandingInspectionService()

    with pytest.raises(TypeError):
        service.inspect_attestation(
            execution_standing_inspection_id="STANDING-001",
            attestation="not-an-attestation",
            revocations=(),
            inspected_at=datetime.now(timezone.utc),
        )


def test_service_requires_certification():
    service = ExecutionStandingInspectionService()

    with pytest.raises(TypeError):
        service.inspect_certification(
            execution_standing_inspection_id="STANDING-001",
            certification="not-a-certification",
            revocations=(),
            inspected_at=datetime.now(timezone.utc),
        )


def test_service_requires_revocation_records():
    service = ExecutionStandingInspectionService()

    with pytest.raises(TypeError):
        service.inspect_attestation(
            execution_standing_inspection_id="STANDING-001",
            attestation=make_attestation(),
            revocations=("not-a-revocation",),
            inspected_at=datetime.now(timezone.utc),
        )


def test_inspection_does_not_modify_source_records():
    service = ExecutionStandingInspectionService()

    attestation = make_attestation()
    revocation = make_revocation(
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
    )

    original_attestation_status = attestation.status
    original_revocation_status = revocation.status

    service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=attestation,
        revocations=(revocation,),
        inspected_at=datetime.now(timezone.utc),
    )

    assert attestation.status is original_attestation_status
    assert revocation.status is original_revocation_status


def test_inspection_creates_no_authority():
    service = ExecutionStandingInspectionService()

    inspection = service.inspect_attestation(
        execution_standing_inspection_id="STANDING-001",
        attestation=make_attestation(),
        revocations=(),
        inspected_at=datetime.now(timezone.utc),
    )

    assert not hasattr(inspection, "authorized")
    assert not hasattr(inspection, "admissible")
    assert not hasattr(inspection, "permission")