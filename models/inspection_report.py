from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class InspectionReport:
    """
    Records the outcome of an inspection.

    An inspection report preserves findings, references,
    unknowns, and recommendations.

    It does not make decisions or authorize action.
    """

    report_id: str
    title: str
    summary: str

    evidence_ids: List[str] = field(default_factory=list)
    relationship_ids: List[str] = field(default_factory=list)

    unknowns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    status: str = "Candidate"

    created: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )