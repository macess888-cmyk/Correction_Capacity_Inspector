import pytest

from models.evidence import Evidence
from models.relationship import Relationship

from orchestrators import (
    InspectionPipeline,
    InspectionPipelineResult,
    InspectionSessionRunner,
)

from registries.evidence_registry import EvidenceRegistry
from registries.inspection_report_registry import (
    InspectionReportRegistry,
)
from registries.relationship_registry import (
    RelationshipRegistry,
)

from services.evidence_service import EvidenceService
from services.inspection_report_service import (
    InspectionReportService,
)
from services.relationship_service import (
    RelationshipService,
)


def build_pipeline() -> InspectionPipeline:
    evidence_service = EvidenceService(
        EvidenceRegistry()
    )

    relationship_service = RelationshipService(
        RelationshipRegistry()
    )

    report_service = InspectionReportService(
        InspectionReportRegistry()
    )

    session_runner = InspectionSessionRunner()

    return InspectionPipeline(
        evidence_service=evidence_service,
        relationship_service=relationship_service,
        report_service=report_service,
        session_runner=session_runner,
    )


def test_inspection_pipeline_end_to_end():

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
    )

    assert isinstance(
        result,
        InspectionPipelineResult,
    )

    assert result.status == "Completed"

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

import pytest


def test_inspection_pipeline_duplicate_identifiers_fail_visibly():

    pipeline = build_pipeline()

    evidence = Evidence(
        evidence_id="evd-duplicate-001",
        title="Duplicate Evidence",
        description="Duplicate identifier test.",
        source="Validation Session",
    )

    pipeline.run(
        report_id="report-duplicate-001",
        title="First Run",
        summary="Initial pipeline run.",
        evidence=[evidence],
        relationships=[],
        unknowns=[],
        recommendations=[],
    )

    with pytest.raises(ValueError):
        pipeline.run(
            report_id="report-duplicate-002",
            title="Second Run",
            summary="Duplicate evidence identifier.",
            evidence=[evidence],
            relationships=[],
            unknowns=[],
            recommendations=[],
        )