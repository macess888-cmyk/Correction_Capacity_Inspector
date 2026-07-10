from __future__ import annotations

from dataclasses import dataclass

from models.correction_capacity_assessment import (
    CorrectionCapacityAssessment,
)
from models.evidence import Evidence
from models.inspection_context import InspectionContext
from models.inspection_report import InspectionReport
from models.relationship import Relationship

from orchestrators.inspection_session_runner import (
    InspectionSessionResult,
    InspectionSessionRunner,
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
from services.relationship_service import RelationshipService


@dataclass(slots=True)
class InspectionPipelineResult:
    """
    Structured result returned by the inspection pipeline.

    The result records what occurred during orchestration.
    It does not authorize action or establish truth.
    """

    context: InspectionContext
    session_result: InspectionSessionResult
    evidence_ids: list[str]
    relationship_ids: list[str]
    report: InspectionReport
    assessment: CorrectionCapacityAssessment
    status: str = "Completed"


class InspectionPipeline:
    """
    Coordinates inspection context, evidence, relationships,
    inspection execution, report creation, and assessment creation.

    The pipeline calls services only.

    It does not access registries directly.
    It does not score, decide, authorize, or infer conclusions.
    """

    def __init__(
        self,
        context_service: InspectionContextService,
        evidence_service: EvidenceService,
        relationship_service: RelationshipService,
        report_service: InspectionReportService,
        assessment_service: CorrectionCapacityAssessmentService,
        session_runner: InspectionSessionRunner,
    ) -> None:
        self._context_service = context_service
        self._evidence_service = evidence_service
        self._relationship_service = relationship_service
        self._report_service = report_service
        self._assessment_service = assessment_service
        self._session_runner = session_runner

    def run(
        self,
        context: InspectionContext,
        assessment_id: str,
        report_id: str,
        title: str,
        summary: str,
        evidence: list[Evidence],
        relationships: list[Relationship],
        unknowns: list[str],
        recommendations: list[str],
        assessment_observations: list[str],
        assessment_limitations: list[str],
    ) -> InspectionPipelineResult:
        """
        Execute one explicit inspection pipeline.

        All context, evidence, relationships, unknowns,
        recommendations, observations, and limitations
        must be supplied by the caller.
        """

        self._context_service.create_context(context)

        evidence_ids: list[str] = []

        for evidence_item in evidence:
            self._evidence_service.add_evidence(evidence_item)
            evidence_ids.append(evidence_item.evidence_id)

        relationship_ids: list[str] = []

        for relationship in relationships:
            self._relationship_service.add_relationship(
                relationship
            )
            relationship_ids.append(
                relationship.relationship_id
            )

        session_result = self._session_runner.run()

        report = InspectionReport(
            report_id=report_id,
            title=title,
            summary=summary,
            evidence_ids=evidence_ids,
            relationship_ids=relationship_ids,
            unknowns=list(unknowns),
            recommendations=list(recommendations),
        )

        self._report_service.add_report(report)

        assessment = CorrectionCapacityAssessment(
            assessment_id=assessment_id,
            inspection_id=context.inspection_id,
            status="COMPLETED",
            summary=summary,
            observations=list(assessment_observations),
            limitations=list(assessment_limitations),
            metadata={
                "report_id": report.report_id,
            },
        )

        self._assessment_service.create_assessment(
            assessment
        )

        completed_context = (
            self._context_service.complete_context(
                context.inspection_id
            )
        )

        return InspectionPipelineResult(
            context=completed_context,
            session_result=session_result,
            evidence_ids=evidence_ids,
            relationship_ids=relationship_ids,
            report=report,
            assessment=assessment,
        )