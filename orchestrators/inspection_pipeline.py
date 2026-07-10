from dataclasses import dataclass
from typing import List

from models.evidence import Evidence
from models.inspection_report import InspectionReport
from models.relationship import Relationship

from orchestrators.inspection_session_runner import (
    InspectionSessionResult,
    InspectionSessionRunner,
)

from services.evidence_service import EvidenceService
from services.inspection_report_service import (
    InspectionReportService,
)
from services.relationship_service import RelationshipService


@dataclass
class InspectionPipelineResult:
    """
    Structured result returned by the inspection pipeline.

    The result records what occurred during orchestration.
    It does not authorize action or establish truth.
    """

    session_result: InspectionSessionResult
    evidence_ids: List[str]
    relationship_ids: List[str]
    report: InspectionReport
    status: str = "Completed"


class InspectionPipeline:
    """
    Coordinates evidence, relationships, inspection execution,
    and report creation.

    The pipeline calls services only.

    It does not access registries directly.
    It does not make decisions or infer conclusions.
    """

    def __init__(
        self,
        evidence_service: EvidenceService,
        relationship_service: RelationshipService,
        report_service: InspectionReportService,
        session_runner: InspectionSessionRunner,
    ) -> None:
        self._evidence_service = evidence_service
        self._relationship_service = relationship_service
        self._report_service = report_service
        self._session_runner = session_runner

    def run(
        self,
        report_id: str,
        title: str,
        summary: str,
        evidence: List[Evidence],
        relationships: List[Relationship],
        unknowns: List[str],
        recommendations: List[str],
    ) -> InspectionPipelineResult:
        """
        Execute one explicit inspection pipeline.

        All evidence, relationships, unknowns, and recommendations
        must be supplied by the caller.
        """

        evidence_ids: List[str] = []

        for evidence_item in evidence:
            self._evidence_service.add_evidence(evidence_item)
            evidence_ids.append(evidence_item.evidence_id)

        relationship_ids: List[str] = []

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

        return InspectionPipelineResult(
            session_result=session_result,
            evidence_ids=evidence_ids,
            relationship_ids=relationship_ids,
            report=report,
        )