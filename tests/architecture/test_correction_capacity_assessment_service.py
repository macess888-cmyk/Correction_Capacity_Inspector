from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)
from registries.correction_capacity_assessment_registry import (
    CorrectionCapacityAssessmentRegistry,
)
from services.correction_capacity_assessment_service import (
    CorrectionCapacityAssessmentService,
)


def make_assessment(
    assessment_id: str = "assessment-001",
    status: str = "CREATED",
) -> CorrectionCapacityAssessment:
    return CorrectionCapacityAssessment(
        assessment_id=assessment_id,
        inspection_id="inspection-001",
        status=status,
    )


def make_service() -> CorrectionCapacityAssessmentService:
    registry = CorrectionCapacityAssessmentRegistry()
    return CorrectionCapacityAssessmentService(registry)


def test_service_creates_and_gets_assessment() -> None:
    service = make_service()
    assessment = make_assessment()

    service.create_assessment(assessment)

    assert service.get_assessment("assessment-001") is assessment


def test_service_updates_assessment() -> None:
    service = make_service()
    assessment = make_assessment()

    service.create_assessment(assessment)

    assessment.summary = "Updated summary."
    service.update_assessment(assessment)

    assert (
        service.get_assessment("assessment-001").summary
        == "Updated summary."
    )


def test_service_completes_assessment() -> None:
    service = make_service()
    assessment = make_assessment()

    service.create_assessment(assessment)

    completed = service.complete_assessment("assessment-001")

    assert completed.status == "COMPLETED"


def test_service_archives_assessment() -> None:
    service = make_service()
    assessment = make_assessment()

    service.create_assessment(assessment)

    archived = service.archive_assessment("assessment-001")

    assert archived.status == "ARCHIVED"


def test_service_lists_and_counts_assessments() -> None:
    service = make_service()

    first = make_assessment("assessment-001")
    second = make_assessment("assessment-002")

    service.create_assessment(first)
    service.create_assessment(second)

    assert service.list_assessments() == [first, second]
    assert service.count_assessments() == 2


def test_service_reports_assessment_existence() -> None:
    service = make_service()
    assessment = make_assessment()

    service.create_assessment(assessment)

    assert service.assessment_exists("assessment-001") is True
    assert service.assessment_exists("missing") is False