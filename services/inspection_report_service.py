from typing import List, Optional

from models.inspection_report import InspectionReport
from registries.inspection_report_registry import (
    InspectionReportRegistry,
)


class InspectionReportService:
    """
    Coordinates inspection report operations.

    Storage remains owned by the registry.
    """

    def __init__(
        self,
        registry: InspectionReportRegistry,
    ) -> None:
        self._registry = registry

    def add_report(
        self,
        report: InspectionReport,
    ) -> None:
        self._registry.add(report)

    def get_report(
        self,
        report_id: str,
    ) -> Optional[InspectionReport]:
        return self._registry.get_by_id(report_id)

    def get_all_reports(self) -> List[InspectionReport]:
        return self._registry.get_all()