from typing import List, Optional

from contracts import MutableRegistryContract
from models.inspection_report import InspectionReport


class InspectionReportRegistry(MutableRegistryContract):
    """
    Stores and retrieves InspectionReport objects.

    The registry does not interpret findings
    or make decisions.
    """

    def __init__(self) -> None:
        self._reports: List[InspectionReport] = []

    def add(self, report: InspectionReport) -> None:
        self._reports.append(report)

    def get_all(self) -> List[InspectionReport]:
        return list(self._reports)

    def get_by_id(
        self,
        report_id: str,
    ) -> Optional[InspectionReport]:
        for report in self._reports:
            if report.report_id == report_id:
                return report

        return None

    def update(self, report: InspectionReport) -> None:
        for index, existing in enumerate(self._reports):
            if existing.report_id == report.report_id:
                self._reports[index] = report
                return

        raise KeyError(
            f"Inspection report not found: {report.report_id}"
        )

    def remove(self, report_id: str) -> None:
        for index, report in enumerate(self._reports):
            if report.report_id == report_id:
                del self._reports[index]
                return

        raise KeyError(
            f"Inspection report not found: {report_id}"
        )