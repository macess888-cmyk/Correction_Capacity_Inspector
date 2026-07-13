from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_revocation import ExecutionRevocation
from models.execution_revocation_status import (
    ExecutionRevocationStatus,
)


def make_execution_revocation() -> ExecutionRevocation:
    return ExecutionRevocation(
        execution_revocation_id="REVOCATION-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
        reason="supporting evidence no longer satisfies current conditions",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=(
            "ATTESTATION-001",
            "CERT-001",
        ),
        metadata={
            "scope": "current-reliance",
        },
    )


def test_execution_revocation_can_be_created():
    revocation = make_execution_revocation()

    assert revocation.execution_revocation_id == "REVOCATION-001"
    assert revocation.subject_id == "ATTESTATION-001"
    assert revocation.subject_type == "EXECUTION_ATTESTATION"
    assert revocation.status is ExecutionRevocationStatus.REVOKED
    assert revocation.revoked_by == "REVIEWER-001"
    assert revocation.evidence_references == (
        "ATTESTATION-001",
        "CERT-001",
    )
    assert revocation.metadata["scope"] == "current-reliance"


def test_execution_revocation_is_immutable():
    revocation = make_execution_revocation()

    with pytest.raises(FrozenInstanceError):
        revocation.status = ExecutionRevocationStatus.SUSPENDED


def test_execution_revocation_metadata_is_immutable():
    revocation = make_execution_revocation()

    with pytest.raises(TypeError):
        revocation.metadata["scope"] = "changed"


def test_execution_revocation_defensively_copies_metadata():
    metadata = {
        "scope": "current-reliance",
    }

    revocation = ExecutionRevocation(
        execution_revocation_id="REVOCATION-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
        reason="standing withdrawn",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=("ATTESTATION-001",),
        metadata=metadata,
    )

    metadata["scope"] = "changed"

    assert revocation.metadata["scope"] == "current-reliance"


def test_execution_revocation_copies_evidence_references():
    references = [
        "ATTESTATION-001",
    ]

    revocation = ExecutionRevocation(
        execution_revocation_id="REVOCATION-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=ExecutionRevocationStatus.REVOKED,
        reason="standing withdrawn",
        revoked_at=datetime.now(timezone.utc),
        revoked_by="REVIEWER-001",
        evidence_references=references,
        metadata={},
    )

    references.append("CERT-001")

    assert revocation.evidence_references == ("ATTESTATION-001",)


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_revocation_id",
        "subject_id",
        "subject_type",
        "reason",
        "revoked_by",
    ],
)
def test_execution_revocation_rejects_empty_required_text(field_name):
    values = {
        "execution_revocation_id": "REVOCATION-001",
        "subject_id": "ATTESTATION-001",
        "subject_type": "EXECUTION_ATTESTATION",
        "status": ExecutionRevocationStatus.REVOKED,
        "reason": "standing withdrawn",
        "revoked_at": datetime.now(timezone.utc),
        "revoked_by": "REVIEWER-001",
        "evidence_references": ("ATTESTATION-001",),
        "metadata": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionRevocation(**values)


def test_execution_revocation_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionRevocation(
            execution_revocation_id="REVOCATION-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status="REVOKED",
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=("ATTESTATION-001",),
            metadata={},
        )


def test_execution_revocation_rejects_missing_revoked_at():
    with pytest.raises(ValueError):
        ExecutionRevocation(
            execution_revocation_id="REVOCATION-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=None,
            revoked_by="REVIEWER-001",
            evidence_references=("ATTESTATION-001",),
            metadata={},
        )


def test_execution_revocation_requires_subject_reference():
    with pytest.raises(ValueError):
        ExecutionRevocation(
            execution_revocation_id="REVOCATION-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_execution_revocation_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionRevocation(
            execution_revocation_id="REVOCATION-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=(
                "ATTESTATION-001",
                "ATTESTATION-001",
            ),
            metadata={},
        )


def test_execution_revocation_rejects_non_mapping_metadata():
    with pytest.raises(TypeError):
        ExecutionRevocation(
            execution_revocation_id="REVOCATION-001",
            subject_id="ATTESTATION-001",
            subject_type="EXECUTION_ATTESTATION",
            status=ExecutionRevocationStatus.REVOKED,
            reason="standing withdrawn",
            revoked_at=datetime.now(timezone.utc),
            revoked_by="REVIEWER-001",
            evidence_references=("ATTESTATION-001",),
            metadata="invalid",
        )


def test_execution_revocation_contains_no_deletion_behavior():
    revocation = make_execution_revocation()

    assert not hasattr(revocation, "delete")
    assert not hasattr(revocation, "purge")
    assert not hasattr(revocation, "remove")


def test_execution_revocation_contains_no_future_authority():
    revocation = make_execution_revocation()

    assert not hasattr(revocation, "authorized")
    assert not hasattr(revocation, "admissible")
    assert not hasattr(revocation, "permission")