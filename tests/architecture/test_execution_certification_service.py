from datetime import datetime, timezone

import pytest

from models.execution_certification import ExecutionCertification
from models.execution_certification_status import (
    ExecutionCertificationStatus,
)
from services.execution_certification_service import (
    ExecutionCertificationService,
)


def test_service_evaluates_registered_profile():
    service = ExecutionCertificationService()

    def profile_evaluator(evidence_references):
        return (
            ExecutionCertificationStatus.CERTIFIED,
            "all required evidence is present",
            {
                "evidence_count": len(evidence_references),
            },
        )

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=profile_evaluator,
    )

    certification = service.evaluate(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        evidence_references=(
            "INTENT-001",
            "RESULT-001",
            "RECEIPT-001",
        ),
    )

    assert isinstance(certification, ExecutionCertification)
    assert certification.execution_certification_id == "CERT-001"
    assert certification.certification_profile_id == "PROFILE-001"
    assert certification.subject_id == "EXECUTION-001"
    assert (
        certification.status
        is ExecutionCertificationStatus.CERTIFIED
    )
    assert certification.reason == "all required evidence is present"
    assert certification.findings["evidence_count"] == 3


def test_service_records_not_certified_truthfully():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.NOT_CERTIFIED,
            "receipt evidence is missing",
            {
                "receipt_present": False,
            },
        ),
    )

    certification = service.evaluate(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        evidence_references=("INTENT-001", "RESULT-001"),
    )

    assert (
        certification.status
        is ExecutionCertificationStatus.NOT_CERTIFIED
    )
    assert certification.reason == "receipt evidence is missing"


def test_service_records_indeterminate_truthfully():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.INDETERMINATE,
            "provenance evidence is unavailable",
            {
                "provenance_known": False,
            },
        ),
    )

    certification = service.evaluate(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        evidence_references=("INTENT-001",),
    )

    assert (
        certification.status
        is ExecutionCertificationStatus.INDETERMINATE
    )


def test_service_rejects_unknown_profile():
    service = ExecutionCertificationService()

    with pytest.raises(ValueError):
        service.evaluate(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-UNKNOWN",
            subject_id="EXECUTION-001",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            evidence_references=("INTENT-001",),
        )


def test_service_rejects_empty_profile_id():
    service = ExecutionCertificationService()

    with pytest.raises(ValueError):
        service.register_profile(
            certification_profile_id="",
            evaluator=lambda references: (
                ExecutionCertificationStatus.CERTIFIED,
                "evidence is sufficient",
                {},
            ),
        )


def test_service_rejects_non_callable_evaluator():
    service = ExecutionCertificationService()

    with pytest.raises(TypeError):
        service.register_profile(
            certification_profile_id="PROFILE-001",
            evaluator="not-callable",
        )


def test_service_rejects_duplicate_profile_registration():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.CERTIFIED,
            "evidence is sufficient",
            {},
        ),
    )

    with pytest.raises(ValueError):
        service.register_profile(
            certification_profile_id="PROFILE-001",
            evaluator=lambda references: (
                ExecutionCertificationStatus.CERTIFIED,
                "evidence is sufficient",
                {},
            ),
        )


def test_service_rejects_invalid_evaluator_status():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            "CERTIFIED",
            "evidence is sufficient",
            {},
        ),
    )

    with pytest.raises(TypeError):
        service.evaluate(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            evidence_references=("INTENT-001",),
        )


def test_service_rejects_empty_evaluator_reason():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.CERTIFIED,
            "",
            {},
        ),
    )

    with pytest.raises(ValueError):
        service.evaluate(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            evidence_references=("INTENT-001",),
        )


def test_service_rejects_non_mapping_findings():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.CERTIFIED,
            "evidence is sufficient",
            "invalid",
        ),
    )

    with pytest.raises(TypeError):
        service.evaluate(
            execution_certification_id="CERT-001",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            evidence_references=("INTENT-001",),
        )


def test_service_preserves_model_validation():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.CERTIFIED,
            "evidence is sufficient",
            {},
        ),
    )

    with pytest.raises(ValueError):
        service.evaluate(
            execution_certification_id="",
            certification_profile_id="PROFILE-001",
            subject_id="EXECUTION-001",
            evaluated_at=datetime.now(timezone.utc),
            evaluated_by="CERTIFICATION-SERVICE",
            evidence_references=("INTENT-001",),
        )


def test_certification_does_not_authorize_future_execution():
    service = ExecutionCertificationService()

    service.register_profile(
        certification_profile_id="PROFILE-001",
        evaluator=lambda references: (
            ExecutionCertificationStatus.CERTIFIED,
            "evidence is sufficient",
            {},
        ),
    )

    certification = service.evaluate(
        execution_certification_id="CERT-001",
        certification_profile_id="PROFILE-001",
        subject_id="EXECUTION-001",
        evaluated_at=datetime.now(timezone.utc),
        evaluated_by="CERTIFICATION-SERVICE",
        evidence_references=("INTENT-001",),
    )

    assert not hasattr(certification, "authorized")
    assert not hasattr(certification, "admissible")
    assert not hasattr(certification, "permission")