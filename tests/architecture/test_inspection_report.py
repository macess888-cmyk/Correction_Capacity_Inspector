import pytest

from contracts import MutableRegistryContract
from models.inspection_report import InspectionReport
from registries.inspection_report_registry import (
    InspectionReportRegistry,
)
from services.inspection_report_service import (
    InspectionReportService,
)


def make_report(
    report_id: str,
    title: str = "Sample Inspection",
) -> InspectionReport:
    return InspectionReport(
        report_id=report_id,
        title=title,
        summary="Candidate inspection result.",
        evidence_ids=["evd-001"],
        relationship_ids=["rel-001"],
        unknowns=["Future effect remains unknown."],
        recommendations=["Continue inspection."],
    )


def test_inspection_report_creation():

    report = make_report("report-001")

    assert report.report_id == "report-001"
    assert report.title == "Sample Inspection"
    assert report.status == "Candidate"


def test_inspection_report_registry_contract_and_mutation():

    registry = InspectionReportRegistry()

    assert isinstance(registry, MutableRegistryContract)

    original = make_report("report-002")

    registry.add(original)

    assert registry.get_by_id("report-002") == original
    assert registry.get_all() == [original]

    updated = make_report(
        "report-002",
        title="Updated Inspection",
    )

    registry.update(updated)

    assert registry.get_by_id("report-002") == updated
    assert registry.get_all() == [updated]

    registry.remove("report-002")

    assert registry.get_by_id("report-002") is None
    assert registry.get_all() == []


def test_inspection_report_registry_rejects_missing_update_and_remove():

    registry = InspectionReportRegistry()
    missing = make_report("missing")

    with pytest.raises(KeyError):
        registry.update(missing)

    with pytest.raises(KeyError):
        registry.remove("missing")


def test_inspection_report_service_uses_registry():

    registry = InspectionReportRegistry()
    service = InspectionReportService(registry)

    report = make_report("report-003")

    service.add_report(report)

    assert service.get_report("report-003") == report
    assert service.get_all_reports() == [report]