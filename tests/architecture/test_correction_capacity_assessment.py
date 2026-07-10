from datetime import UTC, datetime

from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)


def test_assessment_defaults() -> None:
    assessment = CorrectionCapacityAssessment(
        assessment_id="assessment-001",
        inspection_id="inspection-001",
    )

    assert assessment.assessment_id == "assessment-001"
    assert assessment.inspection_id == "inspection-001"
    assert assessment.status == "CREATED"
    assert assessment.summary == ""
    assert assessment.observations == []
    assert assessment.limitations == []
    assert assessment.metadata == {}
    assert isinstance(assessment.created, datetime)
    assert assessment.created.tzinfo == UTC


def test_assessment_accepts_descriptive_values() -> None:
    assessment = CorrectionCapacityAssessment(
        assessment_id="assessment-002",
        inspection_id="inspection-001",
        status="ACTIVE",
        summary="Correction capacity remains observable.",
        observations=[
            "Evidence is present.",
            "Authority remains unresolved.",
        ],
        limitations=[
            "No execution authority was inspected.",
        ],
        metadata={
            "source": "architecture-test",
        },
    )

    assert assessment.status == "ACTIVE"
    assert assessment.summary == (
        "Correction capacity remains observable."
    )
    assert assessment.observations == [
        "Evidence is present.",
        "Authority remains unresolved.",
    ]
    assert assessment.limitations == [
        "No execution authority was inspected.",
    ]
    assert assessment.metadata == {
        "source": "architecture-test",
    }


def test_assessment_mutable_defaults_are_independent() -> None:
    first = CorrectionCapacityAssessment(
        assessment_id="assessment-001",
        inspection_id="inspection-001",
    )
    second = CorrectionCapacityAssessment(
        assessment_id="assessment-002",
        inspection_id="inspection-002",
    )

    first.observations.append("First observation")
    first.limitations.append("First limitation")
    first.metadata["source"] = "first"

    assert second.observations == []
    assert second.limitations == []
    assert second.metadata == {}