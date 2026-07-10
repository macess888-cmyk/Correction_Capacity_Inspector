from models.inspection_report import InspectionReport
from registries.inspection_report_registry import (
    InspectionReportRegistry,
)
from services.inspection_report_service import (
    InspectionReportService,
)


def test_inspection_report_vertical_slice():

    registry = InspectionReportRegistry()
    service = InspectionReportService(registry)

    report = InspectionReport(
        report_id="report-001",
        title="Sample Inspection",
        summary="Candidate inspection result.",
        evidence_ids=["evd-001"],
        relationship_ids=["rel-001"],
        unknowns=["Future effect remains unknown."],
        recommendations=["Continue inspection."],
    )

    service.add_report(report)

    stored_report = service.get_report("report-001")

    assert stored_report is not None
    assert stored_report.report_id == "report-001"
    assert stored_report.evidence_ids == ["evd-001"]
    assert stored_report.relationship_ids == ["rel-001"]
    assert stored_report.status == "Candidate"
    assert service.get_all_reports() == [report]