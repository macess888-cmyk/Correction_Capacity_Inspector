from datetime import datetime, timezone

import pytest

from models.execution_reliance_evaluation import (
    ExecutionRelianceEvaluation,
)
from models.execution_reliance_status import ExecutionRelianceStatus
from models.execution_standing_inspection import (
    ExecutionStandingInspection,
)
from models.execution_standing_status import ExecutionStandingStatus
from services.execution_reliance_evaluation_service import (
    ExecutionRelianceEvaluationService,
)


def make_standing(
    *,
    status: ExecutionStandingStatus = ExecutionStandingStatus.ACTIVE,
) -> ExecutionStandingInspection:
    governing_record_id = "ATTESTATION-001"

    references = (
        "ATTESTATION-001",
    )

    if status is not ExecutionStandingStatus.ACTIVE:
        governing_record_id = "REVOCATION-001"
        references = (
            "ATTESTATION-001",
            "REVOCATION-001",
        )

    return ExecutionStandingInspection(
        execution_standing_inspection_id="STANDING-001",
        subject_id="ATTESTATION-001",
        subject_type="EXECUTION_ATTESTATION",
        status=status,
        inspected_at=datetime.now(timezone.utc),
        reason="standing inspection completed",
        governing_record_id=governing_record_id,
        evidence_references=references,
        findings={},
    )


def test_service_maps_active_standing_to_reliable():
    service = ExecutionRelianceEvaluationService()

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=make_standing(
            status=ExecutionStandingStatus.ACTIVE,
        ),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert isinstance(evaluation, ExecutionRelianceEvaluation)
    assert evaluation.status is ExecutionRelianceStatus.RELIABLE
    assert evaluation.subject_id == "ATTESTATION-001"
    assert evaluation.standing_inspection_id == "STANDING-001"
    assert evaluation.conditions == ()


@pytest.mark.parametrize(
    "standing_status",
    [
        ExecutionStandingStatus.REVOKED,
        ExecutionStandingStatus.WITHDRAWN,
    ],
)
def test_service_maps_terminal_standing_to_not_reliable(
    standing_status,
):
    service = ExecutionRelianceEvaluationService()

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=make_standing(
            status=standing_status,
        ),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert (
        evaluation.status
        is ExecutionRelianceStatus.NOT_RELIABLE
    )
    assert evaluation.conditions == ()


def test_service_maps_suspended_standing_to_conditional():
    service = ExecutionRelianceEvaluationService()

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=make_standing(
            status=ExecutionStandingStatus.SUSPENDED,
        ),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert (
        evaluation.status
        is ExecutionRelianceStatus.CONDITIONALLY_RELIABLE
    )
    assert evaluation.conditions == (
        "current standing is suspended",
        "manual review is required before reliance",
    )


def test_service_maps_indeterminate_standing_to_indeterminate():
    service = ExecutionRelianceEvaluationService()

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=make_standing(
            status=ExecutionStandingStatus.INDETERMINATE,
        ),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert (
        evaluation.status
        is ExecutionRelianceStatus.INDETERMINATE
    )
    assert evaluation.conditions == ()


def test_service_preserves_evidence_references():
    service = ExecutionRelianceEvaluationService()

    standing = make_standing(
        status=ExecutionStandingStatus.REVOKED,
    )

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=standing,
        evaluated_at=datetime.now(timezone.utc),
    )

    assert evaluation.evidence_references == (
        "ATTESTATION-001",
        "STANDING-001",
        "REVOCATION-001",
    )


def test_service_requires_standing_inspection():
    service = ExecutionRelianceEvaluationService()

    with pytest.raises(TypeError):
        service.evaluate(
            execution_reliance_evaluation_id="RELIANCE-001",
            standing_inspection="not-a-standing-inspection",
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_preserves_model_validation():
    service = ExecutionRelianceEvaluationService()

    with pytest.raises(ValueError):
        service.evaluate(
            execution_reliance_evaluation_id="",
            standing_inspection=make_standing(),
            evaluated_at=datetime.now(timezone.utc),
        )


def test_service_does_not_modify_standing_inspection():
    service = ExecutionRelianceEvaluationService()

    standing = make_standing(
        status=ExecutionStandingStatus.SUSPENDED,
    )

    original_status = standing.status
    original_references = standing.evidence_references

    service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=standing,
        evaluated_at=datetime.now(timezone.utc),
    )

    assert standing.status is original_status
    assert standing.evidence_references == original_references


def test_reliance_evaluation_creates_no_authority():
    service = ExecutionRelianceEvaluationService()

    evaluation = service.evaluate(
        execution_reliance_evaluation_id="RELIANCE-001",
        standing_inspection=make_standing(),
        evaluated_at=datetime.now(timezone.utc),
    )

    assert not hasattr(evaluation, "authorized")
    assert not hasattr(evaluation, "admissible")
    assert not hasattr(evaluation, "permission")