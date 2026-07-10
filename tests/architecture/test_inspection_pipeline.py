import pytest

from models.evidence import Evidence
from models.inspection_context import InspectionContext
from models.relationship import Relationship

from orchestrators import (
    InspectionPipeline,
    InspectionPipelineResult,
    InspectionSessionRunner,
)

from registries.correction_capacity_assessment_registry import (
    CorrectionCapacityAssessmentRegistry,
)
from registries.evidence_registry import EvidenceRegistry
from registries.inspection_context_registry import (
    InspectionContextRegistry,
)
from registries.inspection_report_registry import (
    InspectionReportRegistry,
)
from registries.relationship_registry import (
    RelationshipRegistry,
)

from services.correction_capacity_assessment_service import (
    CorrectionCapacityAssessmentService,
)
from services.evidence_service import EvidenceService
from services.inspection_context_service import (
    InspectionContextService,
)
from services.inspection_report_service import (
    InspectionReportService,
)
from services.relationship_service import (
    RelationshipService,
)


def build_pipeline() -> InspectionPipeline:
    context_service = InspectionContextService(
        InspectionContextRegistry()
    )

    evidence_service = EvidenceService(
        EvidenceRegistry()
    )

    relationship_service = RelationshipService(
        RelationshipRegistry()
    )

    report_service = InspectionReportService(
        InspectionReportRegistry()
    )

    assessment_service = (
        CorrectionCapacityAssessmentService(
            CorrectionCapacityAssessmentRegistry()
        )
    )

    session_runner = InspectionSessionRunner()

    return InspectionPipeline(
        context_service=context_service,
        evidence_service=evidence_service,
        relationship_service=relationship_service,
        report_service=report_service,
        assessment_service=assessment_service,
        session_runner=session_runner,
    )


def make_context(
    inspection_id: str = "inspection-pipeline-001",
) -> InspectionContext:
    return InspectionContext(
        inspection_id=inspection_id,
        subject="Correction capacity runtime",
        scope="Pipeline integration",
        objective="Verify coordinated inspection execution",
        operator="Architecture Test",
    )


def test_inspection_pipeline_end_to_end() -> None:
    pipeline = build_pipeline()

    evidence = Evidence(
        evidence_id="evd-pipeline-001",
        title="Observed Signal",
        description="A candidate signal was recorded.",
        source="Validation Session",
    )

    relationship = Relationship(
        relationship_id="rel-pipeline-001",
        source_id="evd-pipeline-001",
        target_id="report-pipeline-001",
        relationship_type="supports",
    )

    result = pipeline.run(
        context=make_context(),
        assessment_id="assessment-pipeline-001",
        report_id="report-pipeline-001",
        title="Pipeline Validation",
        summary="Candidate runtime result.",
        evidence=[evidence],
        relationships=[relationship],
        unknowns=[
            "Long-term effect remains unknown.",
        ],
        recommendations=[
            "Continue inspection.",
        ],
        assessment_observations=[
            "Evidence and relationship artifacts were recorded.",
        ],
        assessment_limitations=[
            "No decision authority was evaluated.",
        ],
    )

    assert isinstance(
        result,
        InspectionPipelineResult,
    )

    assert result.status == "Completed"

    assert result.context.inspection_id == (
        "inspection-pipeline-001"
    )
    assert result.context.status == "COMPLETED"
    assert result.context.completed is not None

    assert result.evidence_ids == [
        "evd-pipeline-001",
    ]

    assert result.relationship_ids == [
        "rel-pipeline-001",
    ]

    assert result.session_result.completed_stages == [
        "Inspection Started",
    ]

    assert result.report.report_id == (
        "report-pipeline-001"
    )

    assert result.report.evidence_ids == [
        "evd-pipeline-001",
    ]

    assert result.report.relationship_ids == [
        "rel-pipeline-001",
    ]

    assert result.report.unknowns == [
        "Long-term effect remains unknown.",
    ]

    assert result.report.recommendations == [
        "Continue inspection.",
    ]

    assert result.assessment.assessment_id == (
        "assessment-pipeline-001"
    )

    assert result.assessment.inspection_id == (
        "inspection-pipeline-001"
    )

    assert result.assessment.status == "COMPLETED"

    assert result.assessment.observations == [
        "Evidence and relationship artifacts were recorded.",
    ]

    assert result.assessment.limitations == [
        "No decision authority was evaluated.",
    ]

    assert result.assessment.metadata == {
        "report_id": "report-pipeline-001",
    }


def test_inspection_pipeline_duplicate_identifiers_fail_visibly() -> None:
    pipeline = build_pipeline()

    evidence = Evidence(
        evidence_id="evd-duplicate-001",
        title="Duplicate Evidence",
        description="Duplicate identifier test.",
        source="Validation Session",
    )

    pipeline.run(
        context=make_context("inspection-duplicate-001"),
        assessment_id="assessment-duplicate-001",
        report_id="report-duplicate-001",
        title="First Run",
        summary="Initial pipeline run.",
        evidence=[evidence],
        relationships=[],
        unknowns=[],
        recommendations=[],
        assessment_observations=[],
        assessment_limitations=[],
    )

    with pytest.raises(ValueError):
        pipeline.run(
            context=make_context("inspection-duplicate-002"),
            assessment_id="assessment-duplicate-002",
            report_id="report-duplicate-002",
            title="Second Run",
            summary="Duplicate evidence identifier.",
            evidence=[evidence],
            relationships=[],
            unknowns=[],
            recommendations=[],
            assessment_observations=[],
            assessment_limitations=[],
        )


def test_inspection_pipeline_duplicate_context_fails_visibly() -> None:
    pipeline = build_pipeline()

    pipeline.run(
        context=make_context("inspection-shared-001"),
        assessment_id="assessment-shared-001",
        report_id="report-shared-001",
        title="First Context Run",
        summary="Initial context registration.",
        evidence=[],
        relationships=[],
        unknowns=[],
        recommendations=[],
        assessment_observations=[],
        assessment_limitations=[],
    )

    with pytest.raises(ValueError):
        pipeline.run(
            context=make_context("inspection-shared-001"),
            assessment_id="assessment-shared-002",
            report_id="report-shared-002",
            title="Duplicate Context Run",
            summary="Duplicate context identifier.",
            evidence=[],
            relationships=[],
            unknowns=[],
            recommendations=[],
            assessment_observations=[],
            assessment_limitations=[],
        )