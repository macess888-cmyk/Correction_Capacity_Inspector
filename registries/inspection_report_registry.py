from typing import List, Optional

from models.inspection_report import InspectionReport


class InspectionReportRegistry:
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