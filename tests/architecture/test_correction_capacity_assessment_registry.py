import pytest

from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)
from registries.correction_capacity_assessment_registry import (
    CorrectionCapacityAssessmentRegistry,
)


def make_assessment(
    assessment_id: str = "assessment-001",
) -> CorrectionCapacityAssessment:
    return CorrectionCapacityAssessment(
        assessment_id=assessment_id,
        inspection_id="inspection-001",
    )


def test_registry_add_get_exists_and_count() -> None:
    registry = CorrectionCapacityAssessmentRegistry()
    assessment = make_assessment()

    registry.add(assessment)

    assert registry.get("assessment-001") is assessment
    assert registry.exists("assessment-001") is True
    assert registry.count() == 1


def test_registry_list_returns_assessments() -> None:
    registry = CorrectionCapacityAssessmentRegistry()

    first = make_assessment("assessment-001")
    second = make_assessment("assessment-002")

    registry.add(first)
    registry.add(second)

    assert registry.list() == [first, second]


def test_registry_update_replaces_existing_assessment() -> None:
    registry = CorrectionCapacityAssessmentRegistry()
    assessment = make_assessment()

    registry.add(assessment)

    updated = CorrectionCapacityAssessment(
        assessment_id="assessment-001",
        inspection_id="inspection-001",
        status="ACTIVE",
        summary="Updated assessment.",
    )

    registry.update(updated)

    assert registry.get("assessment-001") is updated
    assert registry.get("assessment-001").status == "ACTIVE"


def test_registry_remove_returns_assessment() -> None:
    registry = CorrectionCapacityAssessmentRegistry()
    assessment = make_assessment()

    registry.add(assessment)

    removed = registry.remove("assessment-001")

    assert removed is assessment
    assert registry.exists("assessment-001") is False
    assert registry.count() == 0


def test_registry_rejects_duplicate_identifier() -> None:
    registry = CorrectionCapacityAssessmentRegistry()

    registry.add(make_assessment("assessment-001"))

    with pytest.raises(ValueError):
        registry.add(make_assessment("assessment-001"))


def test_registry_missing_get_raises_key_error() -> None:
    registry = CorrectionCapacityAssessmentRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_registry_missing_update_raises_key_error() -> None:
    registry = CorrectionCapacityAssessmentRegistry()

    with pytest.raises(KeyError):
        registry.update(make_assessment("missing"))


def test_registry_missing_remove_raises_key_error() -> None:
    registry = CorrectionCapacityAssessmentRegistry()

    with pytest.raises(KeyError):
        registry.remove("missing")