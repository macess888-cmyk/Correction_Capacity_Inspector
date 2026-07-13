from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from models.execution_attestation import ExecutionAttestation
from models.execution_attestation_status import (
    ExecutionAttestationStatus,
)


def make_execution_attestation() -> ExecutionAttestation:
    return ExecutionAttestation(
        execution_attestation_id="ATTESTATION-001",
        subject_id="EXECUTION-001",
        certification_id="CERT-001",
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The referenced certification was independently reviewed.",
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


def test_execution_attestation_can_be_created():
    attestation = make_execution_attestation()

    assert attestation.execution_attestation_id == "ATTESTATION-001"
    assert attestation.subject_id == "EXECUTION-001"
    assert attestation.certification_id == "CERT-001"
    assert (
        attestation.status
        is ExecutionAttestationStatus.AFFIRMED
    )
    assert attestation.attested_by == "REVIEWER-001"
    assert attestation.evidence_references == (
        "CERT-001",
        "RECEIPT-001",
    )
    assert attestation.metadata["review_scope"] == "bounded"


def test_execution_attestation_is_immutable():
    attestation = make_execution_attestation()

    with pytest.raises(FrozenInstanceError):
        attestation.status = ExecutionAttestationStatus.DECLINED


def test_execution_attestation_metadata_is_immutable():
    attestation = make_execution_attestation()

    with pytest.raises(TypeError):
        attestation.metadata["review_scope"] = "unbounded"


def test_execution_attestation_defensively_copies_metadata():
    metadata = {
        "review_scope": "bounded",
    }

    attestation = ExecutionAttestation(
        execution_attestation_id="ATTESTATION-001",
        subject_id="EXECUTION-001",
        certification_id="CERT-001",
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=("CERT-001",),
        metadata=metadata,
    )

    metadata["review_scope"] = "changed"

    assert attestation.metadata["review_scope"] == "bounded"


def test_execution_attestation_copies_evidence_references():
    references = [
        "CERT-001",
    ]

    attestation = ExecutionAttestation(
        execution_attestation_id="ATTESTATION-001",
        subject_id="EXECUTION-001",
        certification_id="CERT-001",
        status=ExecutionAttestationStatus.AFFIRMED,
        statement="The certification was reviewed.",
        attested_at=datetime.now(timezone.utc),
        attested_by="REVIEWER-001",
        evidence_references=references,
        metadata={},
    )

    references.append("RECEIPT-001")

    assert attestation.evidence_references == ("CERT-001",)


@pytest.mark.parametrize(
    "field_name",
    [
        "execution_attestation_id",
        "subject_id",
        "certification_id",
        "statement",
        "attested_by",
    ],
)
def test_execution_attestation_rejects_empty_required_text(
    field_name,
):
    values = {
        "execution_attestation_id": "ATTESTATION-001",
        "subject_id": "EXECUTION-001",
        "certification_id": "CERT-001",
        "status": ExecutionAttestationStatus.AFFIRMED,
        "statement": "The certification was reviewed.",
        "attested_at": datetime.now(timezone.utc),
        "attested_by": "REVIEWER-001",
        "evidence_references": ("CERT-001",),
        "metadata": {},
    }

    values[field_name] = ""

    with pytest.raises(ValueError):
        ExecutionAttestation(**values)


def test_execution_attestation_rejects_invalid_status():
    with pytest.raises(TypeError):
        ExecutionAttestation(
            execution_attestation_id="ATTESTATION-001",
            subject_id="EXECUTION-001",
            certification_id="CERT-001",
            status="AFFIRMED",
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_execution_attestation_rejects_missing_attested_at():
    with pytest.raises(ValueError):
        ExecutionAttestation(
            execution_attestation_id="ATTESTATION-001",
            subject_id="EXECUTION-001",
            certification_id="CERT-001",
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=None,
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata={},
        )


def test_execution_attestation_rejects_empty_evidence_reference():
    with pytest.raises(ValueError):
        ExecutionAttestation(
            execution_attestation_id="ATTESTATION-001",
            subject_id="EXECUTION-001",
            certification_id="CERT-001",
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001", ""),
            metadata={},
        )


def test_execution_attestation_rejects_duplicate_references():
    with pytest.raises(ValueError):
        ExecutionAttestation(
            execution_attestation_id="ATTESTATION-001",
            subject_id="EXECUTION-001",
            certification_id="CERT-001",
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=(
                "CERT-001",
                "CERT-001",
            ),
            metadata={},
        )


def test_execution_attestation_rejects_non_mapping_metadata():
    with pytest.raises(TypeError):
        ExecutionAttestation(
            execution_attestation_id="ATTESTATION-001",
            subject_id="EXECUTION-001",
            certification_id="CERT-001",
            status=ExecutionAttestationStatus.AFFIRMED,
            statement="The certification was reviewed.",
            attested_at=datetime.now(timezone.utc),
            attested_by="REVIEWER-001",
            evidence_references=("CERT-001",),
            metadata="invalid",
        )


def test_execution_attestation_contains_no_authority_state():
    attestation = make_execution_attestation()

    assert not hasattr(attestation, "authorized")
    assert not hasattr(attestation, "admissible")
    assert not hasattr(attestation, "permission")


def test_execution_attestation_contains_no_execution_behavior():
    attestation = make_execution_attestation()

    assert not hasattr(attestation, "execute")
    assert not hasattr(attestation, "handler")
    assert not hasattr(attestation, "result_id")